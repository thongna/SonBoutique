# Generated by Django 2.0.5 on 2018-08-17 02:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statisticadmin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
