# Generated by Django 4.2 on 2024-05-29 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_comuna_region_solicitudarriendo_rechazada_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='tipo_de_usuario',
            new_name='tipo_usuario',
        ),
    ]