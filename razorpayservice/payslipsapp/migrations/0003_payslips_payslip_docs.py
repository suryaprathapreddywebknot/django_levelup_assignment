# Generated by Django 4.2.8 on 2023-12-05 12:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payslipsapp', '0002_alter_payslips_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='payslips',
            name='payslip_docs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), default=list, null=True, size=None),
        ),
    ]