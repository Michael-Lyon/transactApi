# Generated by Django 4.0.3 on 2022-03-30 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0002_plan_transactions_referral_profit_personal_tweak'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='tid',
            field=models.CharField(max_length=250),
        ),
    ]
