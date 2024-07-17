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

        users = [
            User(
                username=f"{fake.user_name()}{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                email=fake.unique.email(),
            )
            for _ in range(total)
        ]
        created_users = User.objects.bulk_create(users)
        print(f"created {len(created_users)} users")

        chats = [Chat(user=user) for user in created_users]
        created_chats = Chat.objects.bulk_create(chats)
        print(f"created {len(created_chats)} chats")

        # create random chats and messages
        total_num_messages = 0
        for chat in created_chats:
            other_user = random.choice(
                [x for x in users if x != chat.user]
            )  # avoid a chat talking to himself

            # create random messages for each chat
            num_messages = random.randint(1, 10)
            for _ in range(num_messages):
                message = Message.objects.create(
                    text=fake.text(), from_user=random.choice([other_user, chat.user])
                )
                message.chats.add(chat)
                total_num_messages += 1

        print(f"created {total_num_messages} messages")
