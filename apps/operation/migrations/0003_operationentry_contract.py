# Generated by Django 4.0.10 on 2024-01-24 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_contract_bank'),
        ('operation', '0002_remove_operationentry_bank_remove_operationout_bank'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationentry',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.contract'),
        ),
    ]
