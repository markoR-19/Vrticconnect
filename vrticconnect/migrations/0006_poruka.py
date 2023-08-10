# Generated by Django 4.1.7 on 2023-05-09 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("vrticconnect", "0005_objava_grupa"),
    ]

    operations = [
        migrations.CreateModel(
            name="Poruka",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Tekst_poruka", models.TextField(max_length=1000)),
                ("Datum_objave", models.DateTimeField(verbose_name="date published")),
                (
                    "Autor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "Grupa",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vrticconnect.grupa",
                    ),
                ),
            ],
        ),
    ]
