# Generated by Django 4.1.4 on 2023-01-21 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0002_transferorderitem_transferorder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transferorder',
            old_name='warehouse_raw_materials',
            new_name='warehouse_from',
        ),
        migrations.RenameField(
            model_name='transferorder',
            old_name='warehouse_production',
            new_name='warehouse_to',
        ),
        migrations.AlterField(
            model_name='transferorder',
            name='to_number',
            field=models.CharField(default='TO00001', max_length=10),
        ),
        migrations.AlterField(
            model_name='transferorderitem',
            name='to_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_transfer_order_from', to='invoices.transferorder'),
        ),
    ]
