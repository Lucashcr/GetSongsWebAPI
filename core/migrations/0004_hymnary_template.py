# Generated by Django 4.1.7 on 2023-02-27 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_hymnary_created_at_alter_hymnary_owner_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hymnary',
            name='template',
            field=models.CharField(choices=[('single-column', 'Uma coluna'), ('two-columns', 'Duas colunas'), ('each-song-by-page', 'Uma música por página')], default='single-column', max_length=32, verbose_name='Modelo'),
        ),
    ]
