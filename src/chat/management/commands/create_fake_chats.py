import random
from datetime import datetime

from chat.models import Chat, Message
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker


class Command(BaseCommand):
    help = "Creates fake Chat and Message instances"

    def add_arguments(self, parser):
        parser.add_argument("--total", type=int, help="Number of chats to create")

    def handle(self, *args, **kwargs):
        total = kwargs["total"]
        fake = Faker()

        users = []
        for _ in range(total):
            users.append(
                User.objects.create(
                    username=f"{fake.user_name()}{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                    email=fake.unique.email(),
                )
            )

        # create random chats and messages
        for user in users:
            chat = Chat.objects.create(user=user)
            other_user = random.choice(
                [x for x in users if x != user]
            )  # avoid a chat talking to himself

            # create random messages for each chat
            num_messages = random.randint(1, 10)
            for _ in range(num_messages):
                message = Message.objects.create(
                    text=fake.text(), from_user=random.choice([other_user, user])
                )
                message.chats.add(chat)
