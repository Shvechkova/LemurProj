# Generated by Django 4.0.10 on 2024-01-18 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_client_contract'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='contract',
        ),
    ]
