# Generated by Django 3.2.8 on 2021-11-01 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
