# Generated by Django 4.1.4 on 2022-12-18 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_report_report_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='gpd_in_period',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]