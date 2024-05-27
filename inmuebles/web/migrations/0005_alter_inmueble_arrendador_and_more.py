# Generated by Django 4.2 on 2024-05-26 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_populate_database'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inmueble',
            name='arrendador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inmueble_arrendador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inmueble',
            name='arrendatario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inmueble_arrendatario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='solicitudarriendo',
            name='arrendador',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Arrendador'),
        ),
        migrations.AlterField(
            model_name='solicitudarriendo',
            name='inmueble',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.inmueble', verbose_name='Inmueble'),
        ),
    ]
