# Generated by Django 4.2.5 on 2023-09-19 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_prices_cur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prices',
            name='id',
            field=models.DecimalField(decimal_places=0, max_digits=20, primary_key=True, serialize=False),
        ),
    ]
