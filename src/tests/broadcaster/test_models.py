import pytest
from broadcaster.models import Image
from django.core.exceptions import ValidationError
from model_bakery import baker


@pytest.mark.django_db
class TestImage:
    def test_mandatory_fields(self):
        with pytest.raises(ValidationError) as error:
            Image.objects.create()

        assert list(error.value.error_dict.keys()) == ["url"]

    def test_unique_url(self):
        """Making sure that no duplicated urls can happen"""
        image = baker.make(Image)
        with pytest.raises(ValidationError) as error:
            Image.objects.create(url=image.url)

        assert error.value.error_dict["url"][0].messages == [
            "Image with this Url already exists."
        ]

    def test_valid(self):
        image = Image.objects.create(url="http://google.com")
        expected = {
            "id": image.id,
            "created": image.created,
            "modified": image.modified,
            "url": image.url,
        }

        for field in [field.name for field in Image._meta.get_fields()]:
            assert getattr(image, field) == expected[field]
