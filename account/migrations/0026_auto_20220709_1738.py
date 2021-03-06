# Generated by Django 2.2.15 on 2022-07-09 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_auto_20220709_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachingexp',
            name='doc_yrs',
            field=models.IntegerField(blank=True, null=True, verbose_name='Doctoral Research'),
        ),
        migrations.AddField(
            model_name='teachingexp',
            name='postdoc_yrs',
            field=models.IntegerField(blank=True, null=True, verbose_name='Post-doctoral Research'),
        ),
        migrations.AlterField(
            model_name='account',
            name='catg',
            field=models.CharField(blank=True, choices=[(None, 'Select'), ('cast-1', 'SC'), ('cast-2', 'ST'), ('cast-3', 'OBC-A'), ('cast-4', 'OBC-B'), ('cast-5', 'GEN')], max_length=6, null=True, verbose_name='Category'),
        ),
    ]
