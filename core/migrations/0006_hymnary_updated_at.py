# Generated by Django 4.0.4 on 2023-09-21 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_hymnarysong_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='hymnary',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
    ]
