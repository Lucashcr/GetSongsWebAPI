# Generated by Django 4.1.6 on 2023-02-16 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_hymnarysong_alter_hymnary_songs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hymnary',
            name='songs',
        ),
    ]
