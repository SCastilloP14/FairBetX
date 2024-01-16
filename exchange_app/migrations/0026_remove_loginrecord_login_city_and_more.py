# Generated by Django 4.2.1 on 2024-01-16 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_app", "0025_loginrecord"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="loginrecord",
            name="login_city",
        ),
        migrations.RemoveField(
            model_name="loginrecord",
            name="login_country",
        ),
        migrations.AddField(
            model_name="loginrecord",
            name="fit_to_play_acknowledgement",
            field=models.BooleanField(default=True),
        ),
    ]
