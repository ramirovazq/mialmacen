# Generated by Django 2.1.7 on 2019-03-18 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('llantas', '0009_movimiento_observacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Llanta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dot', models.CharField(blank=True, max_length=100, null=True)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='llantas.Marca')),
                ('medida', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='llantas.Medida')),
                ('posicion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='llantas.Posicion')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='llantas.Status')),
            ],
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='dot',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='marca',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='medida',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='posicion',
        ),
        migrations.RemoveField(
            model_name='movimiento',
            name='status',
        ),
    ]