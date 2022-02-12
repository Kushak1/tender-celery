import requests
from bs4 import BeautifulSoup
from celery import Celery
import xmltodict

app = Celery('tasks', broker='redis://localhost:6379', backend='rpc')

class Get_page(app.Task):

    name = 'tasks.get_page'

    def run(self, url):

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
        req = requests.request("GET", url, headers=header)
        
        return req.text

class Get_xml_data(app.Task):

    name = 'tasks.get_xml_data'

    def run(self, html_str):
        
        
        tender_info = []

        soup = BeautifulSoup(html_str, 'html.parser')
        icon_links = soup.find_all("div", {"class": "w-space-nowrap ml-auto registry-entry__header-top__icon"})

        for icon in icon_links:

            data_href = icon.select('a')[1]['href']
            xml_url  = 'https://zakupki.gov.ru/'+data_href.replace('view', 'viewXml')

            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
            req = requests.request("GET", xml_url, headers=header)
            doc = xmltodict.parse(req.text)
            
            #Беру объект через iter next, т.к. ключ первого значения бывает разный
            first_key = next(iter(doc.values()))

            #Чекал разные тендары и нигде не было поля "docPublishDate", поэтому заменил на "plannedPublishDate"
            try:
                tender_date = first_key['commonInfo']['plannedPublishDate']
            except Exception:
                tender_date = None

            tender_info.append({'xml_url':xml_url,'date':tender_date})

        return tender_info

app.register_task(Get_page())
app.register_task(Get_xml_data())