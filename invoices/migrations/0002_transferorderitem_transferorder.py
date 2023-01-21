# Generated by Django 4.1.4 on 2023-01-21 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_category_name'),
        ('companies', '0007_company_warehouse'),
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_with_to', to='products.product')),
                ('to_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_transfer_order_from', to='invoices.workorder')),
            ],
        ),
        migrations.CreateModel(
            name='TransferOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_number', models.CharField(default='WO00001', max_length=10)),
                ('date', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_transfer_order', to='companies.company')),
                ('warehouse_production', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_order_to_warehouse', to='companies.warehouse')),
                ('warehouse_raw_materials', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_order_from_warehouse', to='companies.warehouse')),
            ],
        ),
    ]
