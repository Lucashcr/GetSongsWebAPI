# Generated by Django 4.1.6 on 2023-02-14 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rename_lyrics_song_lyrics_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='lyrics_url',
            field=models.CharField(max_length=256),
        ),
    ]
