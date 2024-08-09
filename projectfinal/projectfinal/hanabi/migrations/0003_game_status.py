# Generated by Django 5.0.6 on 2024-08-09 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hanabi', '0002_remove_game_duration_game_numplayers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.PositiveBigIntegerField(choices=[(1, 'New'), (3, 'Finished'), (2, 'Active')], default=1),
        ),
    ]
