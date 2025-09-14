# PitTraker/myapp/management/commands/create_admin.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create admin user"

    def handle(self, *args, **options):
        if not User.objects.filter(email="ethan.j.pope09@gmail.com").exists():
            User.objects.create_user(
                username="admin",
                email="ethan.j.pope09@gmail.com",
                password="Ethan-2009",
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS("Admin user created successfully!"))
        else:
            self.stdout.write(self.style.WARNING("Admin user already exists!"))
