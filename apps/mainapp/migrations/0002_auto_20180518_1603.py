# Generated by Django 2.0.5 on 2018-05-18 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='travels',
            old_name='joied_users',
            new_name='joined_users',
        ),
    ]
