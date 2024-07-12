import pytest
from chat.models import Chat, Message
from django.core.exceptions import ValidationError
from model_bakery import baker


@pytest.mark.django_db
class TestChat:
    def test_valid(self):
        chat = Chat.objects.create()
        expected = {
            "created": chat.created,
            "modified": chat.modified,
            "id": chat.id,
            "messages": chat.messages,
        }

        for field in [field.name for field in Chat._meta.get_fields()]:
            assert getattr(chat, field) == expected[field]


@pytest.mark.django_db
class TestMessage:
    def test_mandatory_fields(self):
        with pytest.raises(ValidationError) as error:
            Message.objects.create()

        assert list(error.value.error_dict.keys()) == ["chat", "text"]

    def test_valid(self):
        chat = baker.make(Chat)
        message = Message.objects.create(chat=chat, text="foo")
        expected = {
            "id": message.id,
            "created": message.created,
            "modified": message.modified,
            "chat": chat,
            "text": message.text,
            "image": message.image,
        }

        for field in [field.name for field in Message._meta.get_fields()]:
            assert getattr(message, field) == expected[field]
