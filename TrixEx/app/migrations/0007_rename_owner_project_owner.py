# Generated by Django 5.0.1 on 2024-01-13 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='Owner',
            new_name='owner',
        ),
    ]