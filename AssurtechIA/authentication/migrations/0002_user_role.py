# Generated by Django 5.1.5 on 2025-01-23 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('customer', 'Customer')], default='customer', max_length=30, verbose_name='Rôle'),
        ),
    ]
