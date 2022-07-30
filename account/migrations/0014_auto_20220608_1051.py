# Generated by Django 2.2.15 on 2022-06-08 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_account_doc_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='academic',
            name='doc_link',
            field=models.CharField(blank=True, max_length=700, null=True, verbose_name='Document Link'),
        ),
        migrations.AlterField(
            model_name='academic',
            name='degree',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Degree/Certificate'),
        ),
    ]
