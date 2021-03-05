from lxml.html import fromstring
import requests
from requests.exceptions import ConnectionError
import pandas as pd
from urllib.parse import urljoin
import re

URL = r'https://culture.gov.ru/about/subordinates/'

class Minkult_scrapper(object):

    base_url = r'https://culture.gov.ru'

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
        self.refs = html_element.xpath('//div[@class="b-subordinate"]//li//a/@href')

    def _parse_structure(self, html_element, url):
        pattern_address = re.compile(r'\d{6}\,')
        # pattern_phone = re.compile(r'\d{3}[-, ),\s]\d{3}')
        comp_name = html_element.xpath('//div[@class="b-default__title"]/text()')
        data = html_element.xpath('//div[@class="b-administartion__contact-item"]/text()')
        address, phone = [], []
        for elem in data:
            try:
                if re.search(pattern_address, elem).group(0) is not None:
                    address.append(elem)
            except AttributeError:
                pass
            # try:
            #     if re.search(pattern_phone, elem).group(0) is not None:
            #         phone.append(elem)
            # except AttributeError:
            #     pass

        comp_addr = list(zip(comp_name, address))
        return comp_addr

    def run(self):
        self._parse_refs()
        companies = []
        for ref in self.refs:
            full_ref = urljoin(self.base_url, ref)
            try:
                response = self._get_request(full_ref)
                html_element = self._create_html_element(response)
                comp_profile = self._parse_structure(html_element, full_ref)
                companies.extend(comp_profile)
            except ConnectionError:
                pass
        self._save(companies)

    def _save(self, data):
        columns = ['Company', 'Address']
        df = pd.DataFrame(data=data,
                          columns=columns)
        df.to_excel('Minkult.xlsx')


scrapper = Minkult_scrapper()
scrapper.run()



