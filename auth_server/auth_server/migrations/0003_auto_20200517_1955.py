# Generated by Django 3.0.6 on 2020-05-17 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_server', '0002_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='token',
            old_name='token',
            new_name='access',
        ),
    ]
