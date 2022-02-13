import requests
from bs4 import BeautifulSoup
from celery import Celery
import xmltodict

app = Celery('tasks', broker='redis://localhost:6379', backend='rpc')

class Requests:
    def __init__(self):
        
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}

    def request_page(self, url):

        req = requests.request("GET", url, headers=self.header)
        return req

class Get_page(app.Task,Requests):

    name = 'tasks.get_page'

    def run(self, url):

        
        req = self.request_page(url)
    
        soup = BeautifulSoup(req.text, 'html.parser')
        icon_links = soup.find_all("div", {"class": "w-space-nowrap ml-auto registry-entry__header-top__icon"})
        url_arr = []

        for icon in icon_links:
            
            data_href = icon.select('a')[1]['href']
            xml_url  = 'https://zakupki.gov.ru/'+data_href.replace('view', 'viewXml')
            url_arr.append(xml_url)
            
        return url_arr

class Get_xml_data(app.Task, Requests):

    name = 'tasks.get_xml_data'

    def run(self, xml_url):
        

        req = self.request_page(xml_url)
        doc = xmltodict.parse(req.text)
            
        #Беру объект через iter next, т.к. ключ первого значения бывает разный
        first_key = next(iter(doc.values()))

        #Чекал разные тендары и нигде не было поля "docPublishDate", поэтому заменил на "plannedPublishDate"
        try:
            tender_date = first_key['commonInfo']['plannedPublishDate']
        except Exception:
            tender_date = None

        data_dict = {'xml_url':xml_url,'date':tender_date}

        return data_dict

app.register_task(Get_page())
app.register_task(Get_xml_data())