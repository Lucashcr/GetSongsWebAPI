# Generated by Django 4.1.6 on 2023-02-13 16:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_artists_artist_rename_categories_category_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_rename_hymns_hymnaries'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Hymnaries',
            new_name='Hymnary',
        ),
    ]
