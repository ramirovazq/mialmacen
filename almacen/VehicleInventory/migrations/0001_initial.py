# Generated by Django 2.1.1 on 2019-01-23 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_make', models.CharField(max_length=300, null=True)),
                ('vehicle_model', models.CharField(max_length=300, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('color', models.CharField(max_length=300, null=True)),
                ('doors', models.PositiveSmallIntegerField(default=2)),
                ('lot_number', models.CharField(max_length=300, null=True)),
            ],
        ),
    ]
