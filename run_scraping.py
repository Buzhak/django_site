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
from django.contrib.auth import get_user_model
from django.db import DatabaseError
from scraping.parsers import hh
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()

def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst

def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []

    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls

settings = get_settings()
url_list = get_urls(settings)
jobs, errors = [], []

for data in url_list:
    url = list(data['url_data'].values())[0] #достаю единственное значение из вложенного словаря с url адресом
    # parsers = hh('https://khimki.hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=Python+junior&clusters=true&ored_clusters=true&enable_snippets=true')
    parsers = hh(url, city=data['city'], language=data['language'])
    jobs += parsers[0]
    errors += parsers[1]

# city = City.objects.filter(slug='khimki').first() # .first() - нужно для того, чтобы получить инстанс 
# language = Language.objects.filter(slug='python').first()

for job in jobs:
    vacancy = Vacancy(**job)

    try:
        vacancy.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()

# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()