# Generated by Django 2.1.7 on 2019-03-11 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0001_initial'),
        ('llantas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='destino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='destino_del_movimiento', to='persona.Profile'),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='origen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='origen_del_movimiento', to='persona.Profile'),
        ),
    ]
