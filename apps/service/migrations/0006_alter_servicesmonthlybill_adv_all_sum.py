# Generated by Django 4.0.10 on 2024-02-26 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_alter_servicesmonthlybill_adv_all_sum_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesmonthlybill',
            name='adv_all_sum',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='сумма ведения для адв'),
        ),
    ]
