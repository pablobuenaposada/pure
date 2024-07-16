import requests
from chat.models import Chat, Message
from django.core.files.base import ContentFile
from django.db import transaction

from .constants import API_URL, PHOTOS_LIMIT
from .exceptions import NoNewImageFound
from .models import Image


def broadcast_banner_message(user):
    offset = 0
    found = False

    while not found:
        response = requests.get(f"{API_URL}?limit={PHOTOS_LIMIT}&offset={offset}")
        response.raise_for_status()
        images = response.json()

        for image in images["photos"]:
            url = image["url"]
            if not Image.objects.filter(url=url).exists():
                # get image content
                image_content = requests.get(url)
                image_content.raise_for_status()

                with transaction.atomic():
                    # create the new broadcast message
                    message = Message(from_user=user)
                    message.image.save(
                        url.split("/")[-1],
                        ContentFile(image_content.content),
                        save=True,
                    )
                    message.chats.set(Chat.objects.all())

                    # store that this image has been already used
                    Image.objects.create(url=url)

                found = True
                break

        if not found:
            # if we can go for the next offset
            if offset + 1 <= images["total_photos"] / PHOTOS_LIMIT:
                offset += 1
            else:  # this means we know there's no photos we can use
                raise NoNewImageFound
