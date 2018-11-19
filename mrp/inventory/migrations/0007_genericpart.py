# Generated by Django 2.1.2 on 2018-10-31 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20181031_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericPart',
            fields=[
                ('part_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='inventory.Part')),
                ('binLocation', models.CharField(max_length=30)),
                ('inventoryNumber', models.IntegerField()),
                ('inStock', models.IntegerField()),
                ('package', models.CharField(max_length=30)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('inventory.part',),
        ),
    ]