# Generated by Django 4.1.4 on 2022-12-10 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0003_warehouse'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_number', models.CharField(default='TR1', max_length=11)),
                ('tax_date', models.DateField()),
                ('type', models.CharField(choices=[('1', 'BTW'), ('2', 'Nature Tax'), ('3', 'Income Tax'), ('4', 'Citizen Taxes')], default='BTW', max_length=10)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('taxes_paid', models.BooleanField()),
                ('taxes_paid_confirmed', models.BooleanField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tax_payer', to='companies.company')),
            ],
        ),
    ]
