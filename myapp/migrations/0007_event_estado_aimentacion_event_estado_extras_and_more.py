# Generated by Django 5.0.4 on 2024-04-28 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_merge_20240428_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='estado_aimentacion',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='estado_extras',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='estado_transporte',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]