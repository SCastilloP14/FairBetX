# Generated by Django 4.2.1 on 2023-11-29 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_app", "0002_alter_game_game_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="trade",
            old_name="trade_trade_id",
            new_name="trade_id",
        ),
    ]