# Generated by Django 4.0.4 on 2023-10-07 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_alter_hymnarysong_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="hymnary",
            name="file",
            field=models.FileField(
                blank=True, null=True, upload_to="hymnaries/", verbose_name="Arquivo"
            ),
        ),
    ]
