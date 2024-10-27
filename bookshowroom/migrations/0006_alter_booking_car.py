# Generated by Django 5.1.2 on 2024-10-27 04:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshowroom', '0005_alter_booking_id'),
        ('cars', '0004_alter_car_created_at_alter_car_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='car',
            field=models.ForeignKey(default='b66f1758a5c64490a7b463371e6f41a9', on_delete=django.db.models.deletion.CASCADE, to='cars.car'),
            preserve_default=False,
        ),
    ]
