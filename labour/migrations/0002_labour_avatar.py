# Generated by Django 3.1.6 on 2024-03-06 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labour', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='labour',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='labour/avatars/'),
        ),
    ]