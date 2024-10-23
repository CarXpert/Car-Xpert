# Generated by Django 5.1.2 on 2024-10-23 02:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_remove_car_ucd_id'),
        ('comparecars', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompareCarUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comparecaruser_car_one', to='cars.car')),
                ('car_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comparecaruser_car_two', to='cars.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Car',
        ),
    ]
