import pytest
from chat.models import Chat, Message
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from model_bakery import baker


@pytest.mark.django_db
class TestChat:
    def test_mandatory_fields(self):
        """User field is mandatory"""
        with pytest.raises(IntegrityError) as error:
            Chat.objects.create()

        assert "user_id" in error.value.args[0]

    def test_chat_unique_user(self):
        """Only one chat with specific user is allowed"""
        user = baker.make(User)
        Chat.objects.create(user=user)

        with pytest.raises(IntegrityError):
            Chat.objects.create(user=user)

    def test_valid(self):
        user = baker.make(User)
        chat = Chat.objects.create(user=user)
        expected = {
            "created": chat.created,
            "modified": chat.modified,
            "id": chat.id,
            "messages": chat.messages,
            "user": user,
        }

        for field in [field.name for field in Chat._meta.get_fields()]:
            assert getattr(chat, field) == expected[field]


@pytest.mark.django_db
class TestMessage:
    def test_mandatory_fields(self):
        with pytest.raises(ValidationError) as error:
            Message.objects.create()

        assert list(error.value.error_dict.keys()) == ["chat", "text", "from_user"]

    def test_valid(self):
        chat = baker.make(Chat)
        user = baker.make(User)
        message = Message.objects.create(chat=chat, text="foo", from_user=user)
        expected = {
            "id": message.id,
            "created": message.created,
            "modified": message.modified,
            "chat": chat,
            "text": message.text,
            "image": message.image,
            "from_user": user,
        }

        for field in [field.name for field in Message._meta.get_fields()]:
            assert getattr(message, field) == expected[field]
