# Generated by Django 4.1.4 on 2022-12-18 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_number',
            field=models.CharField(default=1, max_length=10, primary_key=True, serialize=False),
        ),
    ]
