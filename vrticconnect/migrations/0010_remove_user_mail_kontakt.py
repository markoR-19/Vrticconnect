# Generated by Django 4.1.7 on 2023-08-08 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vrticconnect", "0009_fotografija"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="Mail_kontakt",
        ),
    ]
