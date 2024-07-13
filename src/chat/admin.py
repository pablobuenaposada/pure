from django.contrib import admin

from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created"]
    search_fields = ["id"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ["chat", "text", "image", "from_user"]
    list_display = ["id", "chat", "from_user"]
    search_fields = ["chat__id"]
    autocomplete_fields = ["chat"]
