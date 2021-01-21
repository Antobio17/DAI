# Generated by Django 3.1.4 on 2020-12-14 00:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mi_aplicacion', '0013_auto_20201211_1842'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ejemplar',
            options={},
        ),
        migrations.RemoveField(
            model_name='ejemplar',
            name='devolucion',
        ),
        migrations.RemoveField(
            model_name='ejemplar',
            name='prestatario',
        ),
        migrations.RemoveField(
            model_name='prestamo',
            name='fecha',
        ),
        migrations.RemoveField(
            model_name='prestamo',
            name='libro',
        ),
        migrations.RemoveField(
            model_name='prestamo',
            name='usuario',
        ),
        migrations.AddField(
            model_name='prestamo',
            name='devolucion',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='prestatario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]