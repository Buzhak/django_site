import codecs
# запускаем django отдельно от проекта 
import os, sys
proj = os.path.dirname(os.path.abspath('manahe.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

import django
django.setup()
# 
from scraping.parsers import hh
from scraping.models import Vacancy, City, Language

parsers = hh()
jobs = parsers[0]
errors = parsers[1]

city = City.objects.filter(slug='khimki')

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()