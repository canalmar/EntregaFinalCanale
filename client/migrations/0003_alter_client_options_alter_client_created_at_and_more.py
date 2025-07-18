# Generated by Django 5.2.2 on 2025-06-21 22:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_client_user_alter_client_address_alter_client_email_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'Client', 'verbose_name_plural': 'Clients'},
        ),
        migrations.AlterField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de alta'),
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(blank=True, help_text='Usuario vinculado; permite login y sincroniza datos básicos.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_record', to=settings.AUTH_USER_MODEL),
        ),
    ]
