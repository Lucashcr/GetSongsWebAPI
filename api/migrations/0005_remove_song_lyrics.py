# Generated by Django 4.0.4 on 2023-08-20 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_song_lyrics"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="song",
            name="lyrics",
        ),
    ]
