# Generated by Django 5.1.6 on 2025-07-20 18:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_contactmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_type', models.CharField(choices=[('phone', 'Telefon'), ('email', 'Email'), ('location', 'Locație'), ('schedule', 'Program')], max_length=20, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('icon_class', models.CharField(help_text='Clasa CSS pentru iconul FontAwesome (ex: fas fa-phone)', max_length=50)),
                ('color_class', models.CharField(help_text='Clasa CSS pentru culoarea gradient (ex: from-blue-400 to-blue-600)', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Ordinea de afișare')),
            ],
            options={
                'verbose_name': 'Contact Info',
                'verbose_name_plural': 'Contact Information',
                'ordering': ['order', 'contact_type'],
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300, verbose_name='Întrebare')),
                ('answer', models.TextField(verbose_name='Răspuns')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activ')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Ordinea de afișare')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'FAQ',
                'ordering': ['order', 'created_at'],
            },
        ),
    ]
