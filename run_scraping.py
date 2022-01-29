import codecs
# запускаем django отдельно от проекта 
import os, sys
from sqlite3 import DatabaseError
proj = os.path.dirname(os.path.abspath('manahe.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django
django.setup()
# 
from django.db import  DatabaseError
from scraping.parsers import hh
from scraping.models import Vacancy, City, Language, Error

parsers = hh()
jobs = parsers[0]
errors = parsers[1]

city = City.objects.filter(slug='khimki').first() # .first() - нужно для того, чтобы получить инстанс 
language = Language.objects.filter(slug='python').first()

for job in jobs:
    vacancy = Vacancy(**job, city=city, language=language)

    try:
        vacancy.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()