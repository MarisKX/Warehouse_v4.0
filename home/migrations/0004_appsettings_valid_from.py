# Generated by Django 4.1.4 on 2023-01-29 22:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_appsettings_acions_per_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='appsettings',
            name='valid_from',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]