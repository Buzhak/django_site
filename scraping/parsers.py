from distutils.log import error
import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
def hh():
    url = 'https://khimki.hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=Python+junior&clusters=true&ored_clusters=true&enable_snippets=true'
    resp = requests.get(url, headers=headers)
    jobs = []
    errors = []
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id = "a11y-main-content")
        if main_div:
            div_list = main_div.find_all('div', attrs={"class":"vacancy-serp-item"})
            for div in div_list:
                job_title = div.find("a", attrs={"class":"bloko-link"})

                job_salary = div.find("div", attrs={"class":"vacancy-serp-item__sidebar"})       
                try:
                    job_salary = job_salary.text
                except AttributeError:
                    job_salary = ""

                title = job_title.text
                href = job_title['href']
                salary = job_salary
                company_name = div.find("a", attrs={"data-qa":"vacancy-serp__vacancy-employer"}).text
                city = div.find("div", attrs={"data-qa":"vacancy-serp__vacancy-address"}).text
                context = div.find("div", attrs={"class":"g-user-content"}).text
                logo = div.find("img")
                jobs.append({'title': title, 'url': href, 'salary': salary, 'company': company_name, 'city': city, 'context': context, 'logo': logo})
        else:
            errors.append({'url': url, 'title': "Main div does not exists"})
    else: 
        errors.append({'url': url, 'title': "Page don't response"})
            


    return jobs, errors

if __name__ == '__main__':
    data_ = hh()
    jobs = data_[0]
    h = codecs.open('work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()