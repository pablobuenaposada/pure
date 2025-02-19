from django.db import models
from django_extensions.db.models import TimeStampedModel


class Image(TimeStampedModel):
    """This model stores used images for broadcast Messages"""

    url = models.URLField(unique=True, blank=False, null=False)

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)
