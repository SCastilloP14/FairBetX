# Generated by Django 4.2.1 on 2023-08-30 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_app", "0015_alter_player_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticker",
            name="payout",
            field=models.IntegerField(default=10),
        ),
    ]
