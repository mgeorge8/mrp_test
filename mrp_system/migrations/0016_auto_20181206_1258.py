# Generated by Django 2.1.2 on 2018-12-06 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mrp_system', '0015_auto_20181206_1257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='location2',
            new_name='location',
        ),
    ]
