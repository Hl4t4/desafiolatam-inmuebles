# Generated by Django 4.2 on 2024-05-26 21:13

from django.db import migrations

def populate_tipo_usuario(apps, schema_editor):
    TipoUsuario = apps.get_model('web', 'TipoUsuario')
    TipoUsuarioChoices = TipoUsuario._meta.get_field('nombre_tipo_usuario')
    for choice in TipoUsuarioChoices.choices:
        TipoUsuario.objects.get_or_create(nombre_tipo_usuario=choice[0])

def populate_tipo_inmueble(apps, schema_editor):
    TipoInmueble = apps.get_model('web', 'TipoInmueble')
    TipoInmuebleChoices = TipoInmueble._meta.get_field('nombre_tipo_inmueble')
    for choice in TipoInmuebleChoices.choices:
        TipoInmueble.objects.get_or_create(nombre_tipo_inmueble=choice[0])

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
        ('web', '0003_alter_usuario_telefono_personal'),
    ]

    operations = [
        migrations.RunPython(populate_tipo_usuario),
        migrations.RunPython(populate_tipo_inmueble),
        migrations.RunPython(populate_region),
        migrations.RunPython(populate_comuna),
    ]
