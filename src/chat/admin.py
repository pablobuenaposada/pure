import requests
from broadcaster.constants import API_URL, PHOTOS_LIMIT
from broadcaster.exceptions import NoNewImageFound
from broadcaster.models import Image
from django.contrib import admin

from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "created"]
    search_fields = ["id"]
    actions = ["send_banner_message"]

    def send_banner_message(self, request, queryset):
        offset = 0
        found = False

        while not found:
            response = requests.get(f"{API_URL}?limit={PHOTOS_LIMIT}&offset={offset}")
            response.raise_for_status()
            images = response.json()

            for image in images["photos"]:
                url = image["url"]
                if not Image.objects.filter(url=url).exists():
                    Image.objects.create(url=url)
                    found = True
                    break

            if not found:
                # if we can go for the next offset
                if offset + 1 <= images["total_photos"] / PHOTOS_LIMIT:
                    offset += 1
                else:  # this means we know there's no photos we can use
                    raise NoNewImageFound


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fields = ["chats", "text", "image", "from_user"]
    list_display = ["id", "from_user"]
    search_fields = ["chats__id"]
    autocomplete_fields = ["chats"]
