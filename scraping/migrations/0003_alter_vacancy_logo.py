# Generated by Django 4.0.1 on 2022-01-29 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_vacancy_logo_vacancy_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='logo',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Ссылка на логотип компании'),
        ),
    ]
