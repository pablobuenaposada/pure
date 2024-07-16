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
        """from_user, and at least one of text or image are mandatory"""
        with pytest.raises(ValidationError) as error:
            Message.objects.create()

        assert set(error.value.error_dict.keys()) == {"from_user", "__all__"}

    def test_either_text_or_image(self):
        """It's mandatory to send or a text or an image or both"""
        Message.objects.create(from_user=baker.make(User), text="foo")
        Message.objects.create(from_user=baker.make(User), image="foo")
        Message.objects.create(from_user=baker.make(User), text="foo", image="foo")

    def test_valid(self):
        user = baker.make(User)
        message = Message.objects.create(text="foo", from_user=user)
        expected = {
            "id": message.id,
            "created": message.created,
            "modified": message.modified,
            "text": message.text,
            "image": message.image,
            "from_user": user,
        }

        for field in {field.name for field in Message._meta.get_fields()} - {"chats"}:
            assert getattr(message, field) == expected[field]
