# Generated by Django 5.1 on 2024-10-18 06:55

import django.db.models.deletion
import fintech_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fintech_app', '0004_remove_wallet_bonus_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='wallet_type',
            field=models.ForeignKey(default=fintech_app.models.get_default_wallet, on_delete=django.db.models.deletion.CASCADE, to='fintech_app.wallettype'),
        ),
    ]