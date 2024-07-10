# project_manager/management/commands/create_default_categories.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from project_manager.models import Category

class Command(BaseCommand):
    help = 'Creates default categories ("Active Projects" and "Archived Projects") for a test user.'

    def handle(self, *args, **options):
        username = 'test_user'
        password = 'password'  # Set your desired password here

        # Check if the test user already exists, otherwise create one
        test_user, created = User.objects.get_or_create(username=username)

        if created:
            test_user.set_password(password)  # Set password for the user
            test_user.save()

            # Create "Active Projects" category for the test user
            active_projects_category = Category.objects.create(user=test_user, name="Active Projects")
            self.stdout.write(self.style.SUCCESS(f'Created category "{active_projects_category}"'))

            # Create "Archived Projects" category for the test user
            archived_projects_category = Category.objects.create(user=test_user, name="Archived Projects")
            self.stdout.write(self.style.SUCCESS(f'Created category "{archived_projects_category}"'))

        else:
            self.stdout.write(self.style.SUCCESS(f'User "{username}" already exists.'))

        self.stdout.write(self.style.SUCCESS(f'Test user created with password: {password}'))
