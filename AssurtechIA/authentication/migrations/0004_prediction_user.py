# Generated by Django 5.1.5 on 2025-01-24 10:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_prediction_alter_user_managers_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
