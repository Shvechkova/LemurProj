# Generated by Django 4.0.10 on 2024-04-17 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0019_remove_categoryoperation_meta_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryoperation',
            name='tes2',
            field=models.CharField(default='none', max_length=200),
        ),
    ]
