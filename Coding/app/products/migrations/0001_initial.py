# Generated by Django 3.2.8 on 2021-10-26 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('brands', '0001_initial'),
        ('subcategories', '0002_rename_subcategories_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('des', models.TextField()),
                ('gender', models.CharField(choices=[('nam', 'NAM'), ('NU', 'NU'), ('KHAC', 'KHAC')], default='nam', max_length=100)),
                ('image_name', models.CharField(max_length=100)),
                ('image_link', models.URLField(max_length=500)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brands.brand')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subcategories.subcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
