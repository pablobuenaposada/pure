from broadcaster.models import Image
from chat.models import Chat, Message
from django.core.files.base import ContentFile
from django.db import transaction
from django_rq import job


@job
def broadcast_image(from_user, message, url, filename, image_content):
    with transaction.atomic():
        # create the new broadcast message
        message = Message(from_user=from_user, text=message)
        message.image.save(filename, ContentFile(image_content), save=True)
        message.chats.set(Chat.objects.all())

        # store that this image has been already used
        Image.objects.create(url=url)
