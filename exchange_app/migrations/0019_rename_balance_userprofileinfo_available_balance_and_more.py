# Generated by Django 4.2.1 on 2023-09-07 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_app", "0018_alter_game_status_alter_ticker_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userprofileinfo",
            old_name="balance",
            new_name="available_balance",
        ),
        migrations.AddField(
            model_name="userprofileinfo",
            name="fees_paid",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="userprofileinfo",
            name="locked_balance",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]