# Generated by Django 3.2.16 on 2023-08-18 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0005_auto_20230818_1901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialattribute',
            name='data_type',
        ),
        migrations.AlterField(
            model_name='materialattributevalue',
            name='value',
            field=models.DecimalField(decimal_places=10, max_digits=20),
        ),
    ]
