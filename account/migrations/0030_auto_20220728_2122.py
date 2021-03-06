# Generated by Django 2.2.15 on 2022-07-28 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0029_account_fwd_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='promo_link',
            field=models.CharField(blank=True, max_length=700, null=True, verbose_name='Document Link'),
        ),
        migrations.AlterField(
            model_name='apicatg_i',
            name='self_api_dt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Self Appraisal Score'),
        ),
    ]
