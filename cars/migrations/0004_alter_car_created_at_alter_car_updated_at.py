# Generated by Django 5.1.2 on 2024-10-27 02:37
from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies = [
        ('cars', '0003_remove_car_ucd_id'),
    ]
    operations = [
        migrations.AlterField(
            model_name='car',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]