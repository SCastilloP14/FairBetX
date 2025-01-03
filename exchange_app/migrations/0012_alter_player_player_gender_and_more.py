# Generated by Django 4.2.1 on 2023-12-08 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange_app", "0011_alter_player_player_height_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="player_gender",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="player_height",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="player_nationality",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="player_position",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="player_sport",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="player_status",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="player",
            name="player_weight",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
