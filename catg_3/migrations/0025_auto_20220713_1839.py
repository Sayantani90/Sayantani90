# Generated by Django 2.2.15 on 2022-07-13 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catg_3', '0024_auto_20220606_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resch_guide',
            name='status',
            field=models.CharField(blank=True, choices=[(None, 'Select'), ('PHDR', 'Ph.D Registered'), ('DEGR', 'Degree awarded'), ('THES', 'Thesis submitted')], max_length=50, null=True, verbose_name='Status'),
        ),
    ]
