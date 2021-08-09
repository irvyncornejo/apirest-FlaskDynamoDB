import requests
from bs4 import BeautifulSoup
import json
import numpy as np

class Scraper:
    def __init__(self):
        self.request = lambda url: requests.get(url)
        self.soup = lambda page: BeautifulSoup(page.text, 'html.parser')
        self.shoes_data = list()

    def get_data_shoes(self):
        types = ['zapatos-slip-on', 'zapatos-era', 'zapatos-old-skool', 'zapatos-sk8-hi', 'zapatos-authentic']
        [self.__get_data_shoe(shoes_type) for shoes_type in types]
        return self.shoes_data
    
    def __get_data_global_shoes(self, shoes_type):
        page_shoes_by_category = self.request(f'https://www.vans.es/shop/es/vans-es/{shoes_type}')
        soup_page_shoes = self.soup(page_shoes_by_category)
        body = soup_page_shoes.find('div', attrs={'id': 'pdp-links-solr'})
        shoes_a = body.find_all('a')
        hrefs = [card.get('href') for card in shoes_a if card.get('href').find('zapatillas') != -1 and card.get('href').find('%') == -1]
        hrefs = np.unique(hrefs)
        return hrefs.tolist()
        
    def __get_data_shoe(self,shoes_type):
        try:
            shoes_link_href = self.__get_data_global_shoes(shoes_type)
            for shoe_link in shoes_link_href[0:5]:
                page_shoe = self.request(shoe_link)
                soup_page_shoe = self.soup(page_shoe)
                id_shoe = soup_page_shoe.find("meta", property="og:productId")['content']
                data_shoe = soup_page_shoe.select_one('span[data-power-reviews-service-options*=prLocale]')
                data_shoe_json = json.loads(data_shoe['data-power-reviews-service-options'])
                data_shoe_json['idShoe'] = id_shoe
                data_shoe_json['typeShoe'] = shoes_type
                self.shoes_data.append(data_shoe_json)
        except Exception as e:
            print(e)