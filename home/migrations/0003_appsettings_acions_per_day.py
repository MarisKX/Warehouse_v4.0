# Generated by Django 4.1.4 on 2023-01-29 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_appsettings_acions_per_day_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appsettings',
            name='acions_per_day',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
