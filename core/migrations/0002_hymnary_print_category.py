# Generated by Django 4.1.7 on 2023-02-19 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="hymnary",
            name="print_category",
            field=models.BooleanField(default=True),
        ),
    ]
