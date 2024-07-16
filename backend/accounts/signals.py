from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Category

@receiver(post_save, sender=CustomUser)
def create_user_categories(sender, instance, created, **kwargs):
    if created:
        default_category = Category.objects.create(user=instance, name="Active Projects")
        archive_category = Category.objects.create(user=instance, name="Archived Projects", locked=True)
        
        instance.default_category = default_category
        instance.archive_category = archive_category
        instance.save()
