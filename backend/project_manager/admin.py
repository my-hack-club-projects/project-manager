from .models import Category
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'locked')

admin.site.register(Category, CategoryAdmin)