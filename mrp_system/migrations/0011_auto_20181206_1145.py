# Generated by Django 2.1.2 on 2018-12-06 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrp_system', '0010_part_document'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='document',
            new_name='datasheet',
        ),
        migrations.AlterField(
            model_name='part',
            name='description',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='part',
            name='partNumber',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
