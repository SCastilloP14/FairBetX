# Generated by Django 4.2.1 on 2023-06-06 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_app", "0006_remove_userprofileinfo_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="status",
            field=models.CharField(
                choices=[
                    ("SCHEDULED", "Scheduled"),
                    ("PLAYING", "Playing"),
                    ("FINISHED", "Finished"),
                    ("CANCELLED", "Cancelled"),
                ],
                default="Scheduled",
                max_length=20,
            ),
        ),
    ]
