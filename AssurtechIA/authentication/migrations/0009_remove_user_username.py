# Generated by Django 5.1.5 on 2025-01-30 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0008_prediction_prediction_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
    ]
