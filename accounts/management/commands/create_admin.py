from django.core.management.base import BaseCommand

from accounts.models import AdminUser


class Command(BaseCommand):
    help = 'Create or update a Smart Travels admin user for the dashboard login'

    def add_arguments(self, parser):
        parser.add_argument('--username', default='admin', help='Admin username')
        parser.add_argument('--password', default='admin123', help='Admin password')
        parser.add_argument('--email', default='info@akisgroup.net', help='Admin email')
        parser.add_argument(
            '--role',
            default=AdminUser.Role.SUPERADMIN,
            choices=[AdminUser.Role.SUPERADMIN, AdminUser.Role.STAFF],
            help='Admin role',
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        role = options['role']

        user, created = AdminUser.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'role': role,
                'is_staff': True,
                'is_active': True,
                'is_superuser': role == AdminUser.Role.SUPERADMIN,
            },
        )

        if not created:
            user.email = email
            user.role = role
            user.is_staff = True
            user.is_active = True
            user.is_superuser = role == AdminUser.Role.SUPERADMIN

        user.set_password(password)
        user.save()

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(
            f'{action} admin user "{username}" ({role}). Login at /admin/login'
        ))
