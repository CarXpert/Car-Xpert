# Generated by Django 5.1.2 on 2024-10-24 06:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_remove_car_ucd_id'),
        ('comparecars', '0002_comparecaruser_delete_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comparecaruser',
            name='car_one',
        ),
        migrations.RemoveField(
            model_name='comparecaruser',
            name='car_two',
        ),
        migrations.CreateModel(
            name='CompareCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compare_car1', to='cars.car')),
                ('car2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compare_car2', to='cars.car')),
            ],
        ),
        migrations.AddField(
            model_name='comparecaruser',
            name='comparecar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comparecars.comparecar'),
        ),
    ]
