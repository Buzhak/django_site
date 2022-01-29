from operator import mod
from pyexpat import model
from re import M
from django.db import models
from .utils import from_cyrillic_to_eng
 

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название населённого пункта', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)


    class Meta:
    
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    
    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)

class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='Язык прогрммироания', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)
    
    class Meta:
        
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    
    def __str__ (self):
        return self.name

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Название вакансии')
    salary = models.CharField(max_length=500, verbose_name='Зарплата', null=True)
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name='Язык программирования')
    # logo = models.CharField(max_length=1000, verbose_name='Ссылка на логотип компании', blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True)
    

    class Meta:
    
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


    def __str__(self):
        return self.title



class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return self.timestamp