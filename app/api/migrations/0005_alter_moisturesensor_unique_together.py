# Generated by Django 5.1.6 on 2025-02-12 22:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_moisuresensor_moisturesensor'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='moisturesensor',
            unique_together={('board', 'sensor_slot')},
        ),
    ]
