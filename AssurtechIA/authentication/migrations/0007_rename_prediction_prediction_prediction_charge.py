# Generated by Django 5.1.5 on 2025-01-27 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_prediction_prediction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prediction',
            old_name='prediction',
            new_name='prediction_charge',
        ),
    ]
