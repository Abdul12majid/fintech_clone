# Generated by Django 5.1 on 2024-10-26 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fintech_app', '0012_alter_transaction_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
    ]
