# Generated by Django 4.0.10 on 2024-01-22 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_rename_сlient_contract_client_contract_date_end_and_more'),
        ('service', '0005_alter_serviceclient_created_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceclient',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.contract'),
        ),
    ]