
import time
from tasks import Get_page,Get_xml_data

class Main:
    def __init__(self):
        #Кол-во страниц для парсинга
        pages_to_parse = 2
        self.parse_pages(pages_to_parse)

    def parse_pages(self,number):
    
        ts = time.time()

        for x in range(0,number):
            url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?fz44=on&pageNumber='+str(x+1)

            page = Get_page().apply_async(args=[url])

            xml_data = Get_xml_data().apply_async(args=[page.get()])

            for data in xml_data.get():
                print('Cсылка на печатную форму: {}; Дата публикации: {};'.format(data['xml_url'], data['date']))

        print('Время выполнения: {} сек.'.format(time.time()-ts))

Main()
    

