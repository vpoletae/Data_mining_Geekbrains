import requests
from pathlib import Path
import bs4
from urllib.parse import urljoin
import pymongo
from datetime import datetime

year = 2021

dates_dict = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 11,
    'декабря': 12,
}


class MagnitParse(object):

    def __init__(self, start_url, db_client):
        self.start_url = start_url
        self.db = db_client['gb_data_mining']
        self.collection = self.db['magnit_products']

    def _get_response(self, url):
        return requests.get(url)

    def _get_soup(self, url):
        response = self._get_response(url)
        return bs4.BeautifulSoup(response.text, 'lxml')

    def run(self):
        soup = self._get_soup(self.start_url)
        catalog = soup.find('div', attrs={'class': "сatalogue__main js-promo-container"})
        for prod_a in catalog.find_all('a', recursive=False):
            product_data = self._parse(prod_a)
            self._save(product_data)

    def _pretty_date(self, date):
        day, month = date.rstrip().lstrip().replace('с ', '').split(' ')
        day = int(day)
        month = dates_dict[month]
        date = datetime(year, month, day)
        return date

    def _find_dates(self, product_a):
        date_from, date_to = product_a.find('div', attrs={'class': "card-sale__date"}
                                        ).text.split('до')
        date_from = self._pretty_date(date_from)
        date_to = self._pretty_date(date_to)
        return (date_from, date_to)

    def _find_prettify_price(self, product_a, tag):
        integer = product_a.find('div', attrs={'class': tag}
                    ).find('span', attrs={'class': "label__price-integer"}).text
        decimal = product_a.find('div', attrs={'class': tag}
                    ).find('span', attrs={'class': "label__price-decimal"}).text
        print(integer)
        print(decimal)
        return float(integer + '.' + decimal)

    def get_template(self):
        return {
            'url': lambda a: urljoin(self.start_url, a.attrs.get('href', '')),
            'promo_name': lambda a: a.find('div', attrs={'class': "card-sale__header"}).text,
            'product_name': lambda a: a.find('div', attrs={'class': "card-sale__title"}).text,
            'old_price': lambda a: self._find_prettify_price(a, "label__price label__price_old"),
            'new_price': lambda a: self._find_prettify_price(a, "label__price label__price_new"),
            'image_url': lambda a: a.find('img')['data-src'], # should be urljoined?
            'date_from': lambda a: self._find_dates(a)[0],
            'date_to': lambda a: self._find_dates(a)[1],
        }

    def _parse(self, product_a):
        data = {}

        for key, func in self.get_template().items():
            try:
                data[key] = func(product_a)
            except (AttributeError, ValueError) as e:
                pass
        return data

    def _save(self, data: dict):
        self.collection.insert_one(data)

def get_save_path(dir_name):
    dir_path = Path(__file__).parent.joinpath(dir_name)
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path

if __name__=='__main__':
    url = "https://magnit.ru/promo/"

    # save_path = get_save_path('magnit_product')
    db_client = pymongo.MongoClient('mongodb://localhost:27017/')
    parser = MagnitParse(url, db_client)
    parser.run()