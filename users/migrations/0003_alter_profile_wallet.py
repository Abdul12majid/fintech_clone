# Generated by Django 5.1 on 2024-10-18 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fintech_app', '0005_alter_wallet_wallet_type'),
        ('users', '0002_profile_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='wallet',
            field=models.ManyToManyField(to='fintech_app.wallettype'),
        ),
    ]