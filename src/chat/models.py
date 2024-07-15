import uuid

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Chat(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Message(TimeStampedModel):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to="message_images/", blank=True, null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)
