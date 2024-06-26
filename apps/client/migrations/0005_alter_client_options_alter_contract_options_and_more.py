# Generated by Django 4.0.10 on 2024-04-04 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('service', '0012_remove_servicesmonthlybill_additional_contract'),
        ('client', '0004_client_manager'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='contract',
            options={'verbose_name': 'Контракт главный', 'verbose_name_plural': 'Контракты главные'},
        ),
        migrations.AlterField(
            model_name='client',
            name='client_name',
            field=models.CharField(max_length=200, verbose_name='имя клиента'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.employee', verbose_name='ответсвенный контракта'),
        ),
        migrations.DeleteModel(
            name='AdditionalContract',
        ),
    ]
