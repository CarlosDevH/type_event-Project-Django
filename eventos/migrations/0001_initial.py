# Generated by Django 4.1.7 on 2023-04-14 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("workload", models.IntegerField()),
                ("logo", models.ImageField(upload_to="logos")),
                ("cor_principal", models.CharField(max_length=7)),
                ("cor_secundaria", models.CharField(max_length=7)),
                ("cor_fundo", models.CharField(max_length=7)),
            ],
        ),
    ]
