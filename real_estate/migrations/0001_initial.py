# Generated by Django 4.1.4 on 2022-12-10 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0003_warehouse'),
    ]

    operations = [
        migrations.CreateModel(
            name='RealEstate',
            fields=[
                ('cadastre_number', models.CharField(default=1, max_length=8, primary_key=True, serialize=False)),
                ('street_adress_1', models.IntegerField(blank=True, default=0, null=True)),
                ('street_adress_2', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('post_code', models.CharField(blank=True, max_length=6)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('field_size', models.IntegerField(blank=True, default=0)),
                ('center_coordinates_min_E', models.IntegerField(default=0)),
                ('center_coordinates_min_S', models.IntegerField(default=0)),
                ('cadastre_value', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='real_estate_owner', to='companies.company')),
            ],
            options={
                'verbose_name_plural': 'Real Estate',
            },
        ),
        migrations.CreateModel(
            name='RealEstateTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('display_name', models.CharField(blank=True, max_length=100)),
                ('color', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Real Estate Types',
            },
        ),
        migrations.CreateModel(
            name='RealEstateCoordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinates_min_E', models.IntegerField(default=0)),
                ('coordinates_min_S', models.IntegerField(default=0)),
                ('coordinates_max_E', models.IntegerField(default=0)),
                ('coordinates_max_S', models.IntegerField(default=0)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('field_size_element', models.IntegerField(blank=True, default=0)),
                ('real_estate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='real_estate', to='real_estate.realestate')),
            ],
        ),
        migrations.AddField(
            model_name='realestate',
            name='property_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='real_estate_type', to='real_estate.realestatetypes'),
        ),
    ]