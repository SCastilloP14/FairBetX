# Generated by Django 4.2.1 on 2023-12-15 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_app", "0021_alter_fill_fill_id_alter_trade_trade_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="position",
            name="position_open_pnl",
        ),
    ]
