# Generated by Django 3.1.6 on 2021-08-14 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0007_auto_20191128_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='maximum',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='minimum',
            field=models.PositiveIntegerField(default=0),
        ),
    ]