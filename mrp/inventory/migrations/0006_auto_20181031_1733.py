# Generated by Django 2.1.2 on 2018-10-31 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20181031_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='name',
            new_name='partNumber',
        ),
    ]
