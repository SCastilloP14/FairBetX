# Generated by Django 4.2.1 on 2023-12-14 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_app", "0019_remove_ticker_ticker_volume"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="ticker",
            name="ticker_last_price",
        ),
    ]
