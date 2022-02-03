import re
from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import FindForm
from .models import Vacancy

# Create your views here.
def home_view(request):
    form = FindForm()
    # city = request.GET.get('city')

    return render(request, 'scraping/home.html', {'form': form})

def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {'city': city, 'language': language, 'form':form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
    
        qs = Vacancy.objects.filter(**_filter) # "**_filter" - передаём словарь с параметрами фильтрации, который был сформирован выше

        paginator = Paginator(qs, 10) # Show 10 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)
