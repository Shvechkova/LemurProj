# Generated by Django 4.0.10 on 2024-02-16 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_remove_servicesmonthlybill_check_entry_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicesmonthlybill',
            name='adv_all_sum',
            field=models.PositiveIntegerField(default='0', verbose_name=''),
        ),
        migrations.AddField(
            model_name='servicesmonthlybill',
            name='chekin_add_subcontr',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='servicesmonthlybill',
            name='chekin_sum_adv',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='servicesmonthlybill',
            name='chekin_sum_entrees',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='servicesmonthlybill',
            name='contract_number',
            field=models.CharField(default=None, max_length=200, verbose_name='название номер контракта'),
        ),
        migrations.AddField(
            model_name='servicesmonthlybill',
            name='contract_sum',
            field=models.PositiveIntegerField(default='0', verbose_name='сумма контракта'),
        ),
        migrations.AddField(
            model_name='servicesmonthlybill',
            name='diff_sum',
            field=models.PositiveIntegerField(default='0', verbose_name='сумма контракта'),
        ),
    ]