from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seed default users including admin and test users'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin'  # 🔐 CHANGE this in production!
            )
            self.stdout.write(self.style.SUCCESS('✅ Admin user created: admin / admin1234'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Admin user already exists.'))

        # Optional: Add test users
        test_users = [
            ('user1', 'user1@gmail.com'),
            ('user2', 'user2@hotmail.com'),
        ]
        for username, email in test_users:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password='123')
                self.stdout.write(self.style.SUCCESS(f'✅ User created: {username} / 123'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ User {username} already exists.'))
