# Generated by Django 3.2.8 on 2021-11-01 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
