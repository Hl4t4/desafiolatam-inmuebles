# Generated by Django 4.2 on 2024-05-27 23:05

from django.db import migrations

def populate_comuna(apps, schema_editor):
    Comuna = apps.get_model('web', 'Comuna')
    ComunaChoices = Comuna._meta.get_field('nombre_comuna')
    for choice in ComunaChoices.choices:
        Comuna.objects.get_or_create(nombre_comuna=choice[0])

def populate_region(apps, schema_editor):
    Region = apps.get_model('web', 'Region')
    RegionChoices = Region._meta.get_field('nombre_region')
    for choice in RegionChoices.choices:
        Region.objects.get_or_create(nombre_region=choice[0])

class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_comuna_nombre_comuna_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_region),
        migrations.RunPython(populate_comuna),
    ]
