# Generated by Django 4.1.4 on 2023-01-29 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('settings_number', models.CharField(default='0000xxxx', max_length=8)),
                ('valid_from', models.DateField()),
                ('valid_till', models.DateField()),
                ('acions_per_day', models.PositiveIntegerField(default=1)),
                ('valid', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Basic Settings',
            },
        ),
    ]