from broadcaster.broadcast import broadcast_banner_message
from django.contrib import admin
from django.shortcuts import render
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .forms import BannerMessageForm
from .models import Chat, Message


class MessageInline(admin.TabularInline):
    model = Message.chats.through
    fields = ["message_id", "message_from_user", "message_text", "message_image"]
    readonly_fields = fields
    extra = 0

    def message_id(self, instance):
        return mark_safe(
            f'<a href="/admin/chat/message/{instance.message.id}">{instance.message.id}</a>'
        )

    def message_text(self, instance):
        return instance.message.text

    def message_image(self, instance):
        return mark_safe(
            f'<img src="{instance.message.image.url}" style="height: 100px"/>'
        )

    def message_from_user(self, instance):
        return instance.message.from_user.username

    message_id.short_description = "Id"
    message_text.short_description = "Text"
    message_image.short_description = "Image"
    message_from_user.short_description = "From User"


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    fields = ["id", "user", "created", "modified"]
    readonly_fields = ["id", "created", "modified"]
    list_display = ["id", "user", "num_messages"]
    search_fields = ["id"]
    actions = ["send_banner_message"]
    inlines = [MessageInline]

    def send_banner_message(self, request, queryset):
        if "message" in request.POST:
            broadcast_banner_message(request.user, request.POST["message"])
        else:
            return render(
                request,
                "admin/send_banner_message.html",
                {"form": BannerMessageForm(), "chat": queryset.first()},
            )

    def num_messages(self, instance):
        return instance.messages.count()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ["chats", "text", "image", "from_user", "created", "modified"]
    list_display = ["id", "from_user", "created", "text", "broadcasted"]
    search_fields = ["chats__id"]
    autocomplete_fields = ["chats"]
    readonly_fields = ["created", "modified"]

    def broadcasted(self, instance):
        """
        If the message is in more than one chat we suppose that the message has been broadcasted
        warning: this is a naive assumption but should be truth in most cases.
        """
        return (
            format_html('<span style="color: green;">&#10004;</span>')
            if instance.chats.count() > 1
            else format_html('<span style="color: red;">&#10008;</span>')
        )
