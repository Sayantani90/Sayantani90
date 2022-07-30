# Generated by Django 2.2.15 on 2022-06-08 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20220608_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='apicatg_i',
            name='url_link',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Put your document link'),
        ),
        migrations.AddField(
            model_name='apicatg_ii',
            name='url_link',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Put your document link'),
        ),
        migrations.AddField(
            model_name='orientation',
            name='url_link',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Put your document link'),
        ),
        migrations.AddField(
            model_name='presentpost',
            name='url_link',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Put your document link'),
        ),
        migrations.AddField(
            model_name='priorpost',
            name='url_link',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Put your document link'),
        ),
        migrations.AddField(
            model_name='teachingexp',
            name='url_link',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Put your document link'),
        ),
    ]
