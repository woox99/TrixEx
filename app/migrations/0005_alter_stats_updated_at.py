# Generated by Django 5.0.1 on 2024-02-02 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_stats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stats',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]