# Generated by Django 3.2.18 on 2023-04-03 13:20

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PrivateModel",
            fields=[
                (
                    "name",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PublicModel",
            fields=[
                (
                    "name",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
            ],
        ),
    ]
