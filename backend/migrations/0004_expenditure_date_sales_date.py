# Generated by Django 5.1.7 on 2025-04-04 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_sales_revenue'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditure',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
