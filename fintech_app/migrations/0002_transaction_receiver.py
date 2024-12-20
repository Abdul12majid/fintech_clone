# Generated by Django 5.1 on 2024-10-17 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fintech_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='fintech_app.wallet'),
            preserve_default=False,
        ),
    ]
