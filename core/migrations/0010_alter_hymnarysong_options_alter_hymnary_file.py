# Generated by Django 4.0.4 on 2023-11-04 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_hymnary_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hymnarysong',
            options={},
        ),
        migrations.AlterField(
            model_name='hymnary',
            name='file',
            field=models.FileField(null=True, upload_to='hymnaries/', verbose_name='Arquivo'),
        ),
    ]
