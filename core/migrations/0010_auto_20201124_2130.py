# Generated by Django 3.1.1 on 2020-11-24 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_item_stockquantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='stockquantity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.stockquantity'),
        ),
    ]
