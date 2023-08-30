# Generated by Django 4.2.1 on 2023-08-26 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_app", "0010_alter_game_away_team_score_and_more"),
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
                    ("POSTPONED", "Postponed"),
                    ("ABD", "Abd"),
                ],
                default="Scheduled",
                max_length=20,
            ),
        ),
    ]
