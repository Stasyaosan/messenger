# Generated by Django 5.0.6 on 2024-08-29 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meow_messenger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/'),
        ),
    ]
