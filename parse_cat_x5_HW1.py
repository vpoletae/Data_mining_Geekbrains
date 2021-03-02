import requests
from pathlib import Path
import time
import json
from parse_x5 import ParseX5


class Parse_cat_X5(ParseX5):

    def __init__(self, start_url: str, save_path: Path):
        '''
        added param for storage of available cats
        '''
        self.start_url = start_url
        self.save_path = save_path
        self.categories = [] # list of dicts

    def _get_categories(self, cat_url):
        '''
        method accepts an URL for cats
        assigns result to cats param
        '''
        response = self._get_response(cat_url)
        self.categories = response.json()

    def _get_response(self, url, params={}):
        while True:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self, cat_url):
        self._get_categories(cat_url)
        for cat_pair in self.categories:
            cat_id = cat_pair['parent_group_code']
            cat_name = cat_pair['parent_group_name']
            cat_products = []
            cat_dict = dict()
            for product in self._parse(self.start_url, cat_id):
                if product:
                    cat_products.append(json.dumps(product))

            cat_dict['name'] = cat_name
            cat_dict['code'] = cat_id
            cat_dict['products'] = cat_products
            cat_path = self.save_path.joinpath(f'{cat_name}.json')
            self._save(cat_dict, cat_path)

    def _parse(self, url, cat_id, params={}):
        params['categories'] = cat_id
        while url:
            response = self._get_response(url, params=params)
            data: dict = response.json()
            url = data['next']
            for product in data['results']:
                yield product

if __name__ == '__main__':
    url = 'https://5ka.ru/api/v2/special_offers/'
    cat_url = 'https://5ka.ru/api/v2/categories/'
    save_path = Path(__file__).parent.joinpath('categories')
    if not save_path.exists():
        save_path.mkdir()

    parser = Parse_cat_X5(url, save_path)
    parser.run(cat_url)

