# Generated by Django 4.1.3 on 2023-11-13 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recognitions', '0002_recognitionmanagermodel_all_start_value'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recognitionmanagermodel',
            old_name='all_start_value',
            new_name='all_stars_value',
        ),
    ]