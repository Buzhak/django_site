# Generated by Django 4.0.1 on 2022-01-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0008_vacancy_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='salary',
            field=models.CharField(max_length=500, null=True, verbose_name='Зарплата'),
        ),
    ]
