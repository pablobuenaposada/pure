import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


class Chat(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Message(TimeStampedModel):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to="message_images/", blank=True, null=True)

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)
