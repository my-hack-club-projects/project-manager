# Generated by Django 5.0.6 on 2024-07-11 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0005_alter_project_name_alter_task_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='duration',
            field=models.IntegerField(default=60),
        ),
        migrations.AlterField(
            model_name='session',
            name='goal',
            field=models.TextField(default='No goal'),
        ),
    ]
