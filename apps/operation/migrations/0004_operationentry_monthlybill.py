# Generated by Django 4.0.10 on 2024-02-09 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_remove_servicesmonthlybill_check_entry_and_more'),
        ('operation', '0003_bankoperation_operationentry_bank_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationentry',
            name='monthlyBill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='service.servicesmonthlybill'),
        ),
    ]
