# Generated by Django 5.1.2 on 2024-10-25 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comparecars', '0004_comparecar_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comparecar',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
