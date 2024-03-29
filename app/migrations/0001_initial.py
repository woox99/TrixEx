# Generated by Django 5.0.1 on 2024-01-20 03:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=26)),
                ('html', models.TextField()),
                ('css', models.TextField()),
                ('js', models.TextField()),
                ('is_public', models.BooleanField()),
                ('is_example', models.BooleanField(default=False)),
                ('is_landing', models.BooleanField(default=False)),
                ('scale', models.FloatField()),
                ('margin_top', models.FloatField()),
                ('margin_left', models.FloatField()),
                ('views', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.project')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=12)),
                ('password', models.TextField()),
                ('motto', models.TextField(default='Hi, I have not yet created a folder encapsultion..')),
                ('is_demo', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('following', models.ManyToManyField(related_name='followers', to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='app.comment')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='app.user')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='bookmarked_users',
            field=models.ManyToManyField(related_name='bookmarked_projects', to='app.user'),
        ),
        migrations.AddField(
            model_name='project',
            name='liked_users',
            field=models.ManyToManyField(related_name='liked_projects', to='app.user'),
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='app.user'),
        ),
        migrations.AddField(
            model_name='comment',
            name='liked_users',
            field=models.ManyToManyField(related_name='liked_comments', to='app.user'),
        ),
        migrations.AddField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.user'),
        ),
    ]
