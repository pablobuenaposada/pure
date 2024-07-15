from unittest.mock import MagicMock, patch

import pytest
from broadcaster.exceptions import NoNewImageFound
from broadcaster.models import Image
from chat.admin import ChatAdmin
from model_bakery import baker


class TestChatAdmin:
    image_url = "http://images.com/1.png"

    @pytest.mark.django_db
    @patch("requests.get")
    def test_send_banner_message_success(self, m_get):
        m_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "total_photos": 1,
                "photos": [{"url": self.image_url}],
            },
        )

        assert Image.objects.all().exists() is False

        ChatAdmin.send_banner_message(ChatAdmin, None, None)

        image = Image.objects.get()
        assert image.url == self.image_url

    @pytest.mark.django_db
    @patch("requests.get")
    def test_send_banner_message_no_new_image(self, m_get):
        """If all the images provided by the API had been already used, an exception should be raised"""
        baker.make(Image, url=self.image_url)
        m_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "total_photos": 1,
                "photos": [{"url": self.image_url}],
            },
        )

        assert Image.objects.count() == 1

        with pytest.raises(NoNewImageFound):
            ChatAdmin.send_banner_message(ChatAdmin, None, None)

        assert Image.objects.count() == 1
