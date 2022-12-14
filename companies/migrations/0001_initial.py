# Generated by Django 4.1.4 on 2022-12-10 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('name', models.CharField(blank=True, max_length=254, null=True)),
                ('full_name', models.CharField(blank=True, max_length=254)),
                ('registration_number', models.PositiveIntegerField(blank=True, default=1, primary_key=True, serialize=False)),
                ('invoice_prefix', models.CharField(max_length=2, unique=True)),
                ('street_adress_1', models.IntegerField(blank=True, default=0)),
                ('street_adress_2', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('post_code', models.CharField(blank=True, max_length=6)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=254, null=True)),
                ('full_name', models.CharField(blank=True, max_length=254)),
                ('warehouse_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_owner', to='companies.company')),
            ],
        ),
        migrations.CreateModel(
            name='StockItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_location', to='companies.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='StockHistoryEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_nr', models.CharField(blank=True, max_length=254, null=True)),
                ('quantity_plus', models.IntegerField(blank=True, default=0, null=True)),
                ('quantity_minus', models.IntegerField(blank=True, default=0, null=True)),
                ('saldo', models.IntegerField(blank=True, default=0, null=True)),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='element', to='companies.stockitem')),
            ],
        ),
    ]
