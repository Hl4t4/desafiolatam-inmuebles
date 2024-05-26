# Generated by Django 4.2 on 2024-05-26 09:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_alter_inmueble_arrendador_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='arrendador',
            field=models.ForeignKey(default=15, on_delete=django.db.models.deletion.PROTECT, related_name='inmueble_arrendador', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='arrendatario',
            field=models.ForeignKey(default=15, on_delete=django.db.models.deletion.PROTECT, related_name='inmueble_arrendatario', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
