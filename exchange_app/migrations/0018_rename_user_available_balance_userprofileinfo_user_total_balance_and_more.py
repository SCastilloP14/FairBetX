# Generated by Django 4.2.1 on 2023-12-12 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_app", "0017_alter_transaction_transaction_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userprofileinfo",
            old_name="user_available_balance",
            new_name="user_total_balance",
        ),
        migrations.RemoveField(
            model_name="userprofileinfo",
            name="user_locked_balance",
        ),
        migrations.AlterField(
            model_name="order",
            name="order_status",
            field=models.CharField(
                choices=[
                    ("OPEN", "Open"),
                    ("PARTIAL", "Partially Filled"),
                    ("FILLED", "Filled"),
                    ("CANCELED", "Canceled"),
                    ("SETTLED", "Settled"),
                    ("TICKER_CANCELED", "Ticker Canceled"),
                ],
                default="OPEN",
                max_length=20,
            ),
        ),
    ]
