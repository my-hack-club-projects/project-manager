from django.contrib.auth.models import AbstractUser, UserManager
from project_manager.models import Category
from django.db import models, transaction

class CustomUserManager(UserManager): # Old, unused, removing breaks migrations
    use_in_migrations = True

    def create_categories(self, user):
        default_category = Category.objects.create(user=user, name="Active Projects")
        default_category.save()
        user.default_category = default_category

        archive_category = Category.objects.create(user=user, name="Archived Projects", locked=True)
        archive_category.save()
        user.archive_category = archive_category

        user.save()

    def create_user(self, username, email=None, password=None, **extra_fields):
        print("Creating user")

        user = super().create_user(username, email, password, **extra_fields)
        self.create_categories(user)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        user = self.create_superuser(username, email, password, **extra_fields)
        self.create_categories(user)
        return user

class CustomUser(AbstractUser):
    default_category = models.OneToOneField(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='default_user')
    archive_category = models.OneToOneField(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='archive_user')