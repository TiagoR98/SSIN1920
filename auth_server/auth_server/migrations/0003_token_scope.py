# Generated by Django 3.0.6 on 2020-05-21 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_server', '0002_auto_20200520_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='scope',
            field=models.CharField(default='bla', max_length=50),
            preserve_default=False,
        ),
    ]
