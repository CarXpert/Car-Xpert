# Generated by Django 5.1.2 on 2024-10-23 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshowroom', '0001_initial'),
        ('cars', '0003_remove_car_ucd_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='time',
        ),
        migrations.AddField(
            model_name='booking',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars.car'),
        ),
        migrations.AddField(
            model_name='booking',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='visit_date',
            field=models.DateField(default='2024-01-01'),
        ),
        migrations.AddField(
            model_name='booking',
            name='visit_time',
            field=models.TimeField(default='12:00:00'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
