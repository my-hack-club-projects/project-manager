from django.contrib.auth.models import AbstractUser
from project_manager.models import Category
from django.db import models

class CustomUser(AbstractUser):
    default_category = models.OneToOneField(Category, on_delete=models.CASCADE, null=True, blank=True)
    archive_category = models.OneToOneField(Category, on_delete=models.CASCADE, null=True, blank=True)

    def save(self):
        self.super.save()

        if self.default_category is None:
            self.default_category = Category.objects.create(user=self, name="Active Projects")
            self.default_category.save()

        if self.archive_category is None:
            self.archive_category = Category.objects.create(user=self, name="Archived Projects", locked=True)
            self.archive_category.save()