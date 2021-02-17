import requests
from pathlib import Path
import time
import json

# params = {
#     'store':None,
#     'records_per_page':12,
#     'page':1,
#     'categories': None,
#     'ordering': None,
#     'price_prome__gte': None,
#     'price_promo_lte': None,
#     'search': None,
# }

# response = requests.get(url, params=params, headers=headers)

# result_html_file = Path(__file__).parent.joinpath('5ka.html')
# result_html_file.write_text(response.text, encoding='UTF-8')

# result_json_file = Path(__file__).parent.joinpath('5ka.json')
# result_json_file.write_text(response.text, encoding='UTF-8')

class ParseX5(object):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}

    def __init__(self, start_url: str, save_path: Path):
        self.start_url = start_url
        self.save_path = save_path

    def _get_response(self, url):
        while True:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.save_path.joinpath(f'{product["id"]}.json')
            self._save(product, product_path)

    def _parse(self, url):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data['next']
            for product in data['results']:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False)) # adjust

if __name__ == '__main__':
    url = 'https://5ka.ru/api/v2/special_offers/'
    save_path = Path(__file__).parent.joinpath('products')
    if not save_path.exists():
        save_path.mkdir()

    parser = ParseX5(url, save_path)
    parser.run()

