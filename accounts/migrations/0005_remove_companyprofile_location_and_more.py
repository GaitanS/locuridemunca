# Generated by Django 5.1.6 on 2025-04-23 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_companyprofile_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyprofile',
            name='location',
        ),
        migrations.RemoveField(
            model_name='jobseekerprofile',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='jobseekerprofile',
            name='location',
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Oraș'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='country',
            field=models.CharField(blank=True, default='România', max_length=100, null=True, verbose_name='Țară'),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='street_address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Adresă sediu social (stradă, număr...)'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='city_of_residence',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Oraș de reședință'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Data nașterii'),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='company_name',
            field=models.CharField(max_length=255, verbose_name='Numele companiei'),
        ),
    ]
