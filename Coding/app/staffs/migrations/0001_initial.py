# Generated by Django 3.2.8 on 2021-10-26 13:46

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format '+8423456789'. Up to 15 digits allowed.", regex='^\\+?84?\\d{9,15}$')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
