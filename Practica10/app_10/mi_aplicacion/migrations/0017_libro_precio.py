# Generated by Django 3.1.5 on 2021-01-19 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_aplicacion', '0016_auto_20201221_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='precio',
            field=models.FloatField(null=True),
        ),
    ]
