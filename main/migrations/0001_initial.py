# Generated by Django 5.1.1 on 2024-10-23 06:57

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShowRoom',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('showroom_name', models.CharField(max_length=30)),
                ('showroom_location', models.TextField()),
                ('showroom_regency', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('brand', models.CharField(max_length=30)),
                ('car_type', models.CharField(max_length=30)),
                ('model', models.CharField(max_length=30)),
                ('color', models.CharField(max_length=30)),
                ('year', models.PositiveIntegerField()),
                ('transmission', models.CharField(max_length=30)),
                ('fuel_type', models.CharField(max_length=30)),
                ('doors', models.PositiveIntegerField()),
                ('cylinder_size', models.PositiveIntegerField()),
                ('cylinder_total', models.PositiveIntegerField()),
                ('turbo', models.BooleanField()),
                ('mileage', models.PositiveIntegerField()),
                ('license_plate', models.CharField(max_length=30)),
                ('price_cash', models.PositiveIntegerField()),
                ('price_credit', models.PositiveIntegerField()),
                ('pkb_value', models.FloatField()),
                ('pkb_base', models.FloatField()),
                ('stnk_date', models.DateField()),
                ('levy_date', models.DateField()),
                ('swdkllj', models.FloatField()),
                ('total_levy', models.FloatField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('showroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.showroom')),
            ],
        ),
    ]