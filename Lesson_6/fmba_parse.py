from lxml.html import fromstring
import requests
from requests.exceptions import ConnectionError
import pandas as pd
import re
from urllib.parse import urljoin

URL = r'https://fmba.gov.ru/o-fmba-rossii/podvedomstvennye-organizatsii/'
pages = 28

class FMBA_scrapper(object):

    base_url = r'https://fmba.gov.ru/'

    def __init__(self):
        self.refs = []

    def _get_new_page(self, url, page, params={}):
        params['PAGEN_1'] = page
        response = requests.get(url, params=params, verify=True)
        return response

    def _get_request(self, url, params={}):
        response = requests.get(url, params=params, verify=True)
        return response

    def _create_html_element(self, response):
        html_element = fromstring(response.text)
        return html_element

    def _parse_refs(self, url, page):
        html_element = self._create_html_element(
            self._get_new_page(url, page)
        )
        self.refs.extend(html_element.xpath('//div/p/a/@href'))

    def _parse_company(self, html_element, url):
        comp_name = html_element.xpath('//div/h3/text()')[0]
        comp_data = html_element.xpath('//div[@class = "news-detail"]/text()')
        address, phone = '', ''
        for elem in comp_data:
            if 'г.' in elem or 'д.' in elem or 'ул.' in elem \
                or 'обл' in elem or 'край' in elem or 'Россия' in elem\
                    or 'улица' in elem:
                address = elem.rstrip().lstrip().replace('\xa0\xa0', '').split(':')[-1]
            elif 'Телеф' in elem:
                phone = elem.rstrip().lstrip().replace('\xa0\xa0', '').split(':')[-1]
            else:
                continue
        return [url, comp_name, address, phone]

    def run(self):
        for page in range(1, pages+1):
            self._parse_refs(URL, page)
        companies = []
        for ref in self.refs:
            full_ref = urljoin(self.base_url, ref)
            try:
                response = self._get_request(full_ref)
                html_element = self._create_html_element(response)
                comp_profile = self._parse_company(html_element, ref)
                companies.append(comp_profile)
            except ConnectionError:
                pass
        self._save(companies)

    def _save(self, data):
        columns = ['URL', 'Company', 'Address', 'Phone']
        df = pd.DataFrame(data=data,
                          columns=columns)
        df.to_excel('FMBA.xlsx')


scrapper = FMBA_scrapper()
scrapper.run()



