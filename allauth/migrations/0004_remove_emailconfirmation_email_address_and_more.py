# Generated by Django 4.1.4 on 2023-02-07 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allauth', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailconfirmation',
            name='email_address',
        ),
        migrations.DeleteModel(
            name='EmailAddress',
        ),
        migrations.DeleteModel(
            name='EmailConfirmation',
        ),
    ]
