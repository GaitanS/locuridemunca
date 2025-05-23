# Generated by Django 5.1.6 on 2025-05-18 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_jobseekerprofile_saved_jobs'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofile',
            name='industry',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Industrie'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Locație sediu principal'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='slug',
            field=models.SlugField(blank=True, help_text='Lăsați necompletat pentru generare automată bazată pe numele companiei.', max_length=255, unique=True),
        ),
    ]
