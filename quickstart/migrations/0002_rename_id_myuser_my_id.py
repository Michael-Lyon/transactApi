# Generated by Django 4.0.3 on 2022-04-25 00:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='id',
            new_name='my_id',
        ),
    ]
