from broadcaster.broadcast import broadcast_banner_message
from django.contrib import admin

from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created"]
    list_display = ["id", "user"]
    search_fields = ["id"]
    actions = ["send_banner_message"]

    def send_banner_message(self, request, queryset):
        broadcast_banner_message(request.user)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ["chats", "text", "image", "from_user", "created", "modified"]
    list_display = ["id", "from_user", "created"]
    search_fields = ["chats__id"]
    autocomplete_fields = ["chats"]
    readonly_fields = ["created", "modified"]
