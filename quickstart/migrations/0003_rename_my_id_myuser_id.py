# Generated by Django 4.0.3 on 2022-04-25 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0002_rename_id_myuser_my_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='my_id',
            new_name='id',
        ),
    ]