# Generated by Django 4.1.3 on 2023-05-04 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('attendance', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weekattendancerolemanager',
            name='users_group',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='Role`s group'),
        ),
    ]
