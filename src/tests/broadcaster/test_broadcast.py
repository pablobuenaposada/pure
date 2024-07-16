from unittest.mock import MagicMock, patch

import pytest
from broadcaster.broadcast import broadcast_banner_message
from broadcaster.exceptions import NoNewImageFound
from broadcaster.models import Image
from chat.models import Message
from django.contrib.auth.models import User
from model_bakery import baker

IMAGE_CONTENT = b"foo"
IMAGE_URL = "http://images.com/1.png"


@pytest.mark.django_db
class TestBroadcast:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.user = baker.make(User)

    def patched_get(self, *args, **kwargs):
        """method to return different http response depending the url"""
        match self:
            case (
                "https://api.slingacademy.com/v1/sample-data/photos?limit=100&offset=0"
            ):
                return MagicMock(
                    status_code=200,
                    json=lambda: {
                        "total_photos": 1,
                        "photos": [{"url": IMAGE_URL}],
                    },
                )
            case "http://images.com/1.png":
                return MagicMock(
                    status_code=200,
                    content=IMAGE_CONTENT,
                )

    @patch("requests.get", new=patched_get)
    def test_broadcast_banner_message_success(self):
        assert Image.objects.all().exists() is False
        assert Message.objects.all().exists() is False

        broadcast_banner_message(self.user)

        assert Image.objects.get().url == IMAGE_URL
        assert Message.objects.get(from_user=self.user).image.read() == IMAGE_CONTENT

    @patch("requests.get", new=patched_get)
    def test_broadcast_banner_message_no_new_image(self):
        """If all the images provided by the API had been already used, an exception should be raised"""
        baker.make(Image, url=IMAGE_URL)
        assert Image.objects.count() == 1
        assert Message.objects.all().exists() is False

        with pytest.raises(NoNewImageFound):
            broadcast_banner_message(self.user)

        assert Image.objects.count() == 1
        assert Message.objects.all().exists() is False
