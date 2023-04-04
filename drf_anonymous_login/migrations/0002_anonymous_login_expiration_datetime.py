# Generated by Django 3.2.18 on 2023-04-03 12:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("drf_anonymous_login", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="anonymouslogin",
            name="expiration_datetime",
            field=models.DateTimeField(
                default=None, null=True, verbose_name="expiration datetime"
            ),
        ),
        migrations.AlterField(
            model_name="anonymouslogin",
            name="created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="created"),
        ),
        migrations.AlterField(
            model_name="anonymouslogin",
            name="token",
            field=models.CharField(
                db_index=True, max_length=64, unique=True, verbose_name="token"
            ),
        ),
    ]