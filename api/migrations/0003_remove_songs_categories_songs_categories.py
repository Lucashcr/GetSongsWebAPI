# Generated by Django 4.1.4 on 2022-12-16 04:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_category_songs_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='songs',
            name='categories',
        ),
        migrations.AddField(
            model_name='songs',
            name='categories',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.categories'),
            preserve_default=False,
        ),
    ]
