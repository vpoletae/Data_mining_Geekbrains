from lxml.html import fromstring
import requests
from requests.exceptions import ConnectionError
import pandas as pd
import re

URL = r'https://minzdrav.gov.ru/ministry/informatsiya-o' \
      r'-podvedomstvennyh-ministerstvu-zdravoohraneniya-' \
      r'rossii-organizatsiyah'

class Minzdrav_scrapper(object):

    def __init__(self):
        self.refs = []

    def _get_request(self, url, params={}):
        response = requests.get(url, params=params, verify=True)
        return response

    def _create_html_element(self, response):
        html_element = fromstring(response.text)
        return html_element

    def _parse_refs(self):
        html_element = self._create_html_element(
            self._get_request(url=URL)
        )
        self.refs = html_element.xpath('//article//a/@href')

    def _parse_company(self, html_element, url):
        comp_name = html_element.xpath('//h1/text()')
        try:
            comp_name = comp_name[0]
        except IndexError:
            pass
        data = html_element.xpath('//p/text()')
        address, phone, email, web = '', '', '', ''
        pattern = re.compile(r'\d{6}')
        for elem in data:
            if 'г.' in elem or 'д.' in elem or 'ул.' in elem \
                    or re.search(pattern, elem) is not None:
                address = elem
            elif '+' in elem:
                phone = elem
            elif '@' in elem:
                email = elem
            elif 'http' in elem or 'www' in elem:
                web = elem
            else:
                continue
        return [url, comp_name, address, phone, email, web]

    def run(self):
        self._parse_refs()
        companies = []
        for ref in self.refs:
            try:
                response = self._get_request(ref)
                html_element = self._create_html_element(response)
                comp_profile = self._parse_company(html_element, ref)
                companies.append(comp_profile)
            except ConnectionError:
                pass
        self._save(companies)

    def _save(self, data):
        columns = ['URL', 'Company', 'Address', 'Phone', 'Email', 'Web']
        df = pd.DataFrame(data=data,
                          columns=columns)
        df.to_excel('Minzdrav.xlsx')


scrapper = Minzdrav_scrapper()
scrapper.run()



