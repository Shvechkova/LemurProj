# Generated by Django 4.0.10 on 2024-02-16 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_servicesmonthlybill_adv_all_sum_and_more'),
        ('operation', '0007_operationout_suborder_alter_operationout_bank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('amount', models.PositiveIntegerField(default='0')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('type_operation', models.CharField(choices=[('entry', 'entry'), ('out', 'out')], default='out', max_length=5)),
                ('bank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='operation.bankoperation')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='operation.categoryoperation', verbose_name='Категория операции')),
                ('meta_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='operation.metacategoryoperation', verbose_name='Главная категория операции')),
                ('monthly_bill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='service.servicesmonthlybill')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='operation.nameoperation', verbose_name='Название операции')),
                ('suborder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='service.subcontractmonth', verbose_name='Субподряд')),
            ],
        ),
    ]
