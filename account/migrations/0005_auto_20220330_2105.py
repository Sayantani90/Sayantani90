# Generated by Django 2.2.15 on 2022-03-30 15:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_apicatg_i'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apicatg_i',
            name='direct_teaching',
            field=models.PositiveIntegerField(blank=True, default=701, null=True, validators=[django.core.validators.MinValueValidator(700)], verbose_name='Hours spent per academic year'),
        ),
        migrations.AlterField(
            model_name='apicatg_i',
            name='exam_duties',
            field=models.IntegerField(blank=True, null=True, verbose_name='Hours spent per academic year'),
        ),
        migrations.AlterField(
            model_name='apicatg_i',
            name='innovating_teaching',
            field=models.IntegerField(blank=True, null=True, verbose_name='Hours spent per academic year'),
        ),
    ]
