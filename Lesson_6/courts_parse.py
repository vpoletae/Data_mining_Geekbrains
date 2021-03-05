from lxml.html import fromstring
import requests
from requests.exceptions import ConnectionError
import pandas as pd
import re
from urllib.parse import urljoin


class Courts_scrapper(object):

    base_url = 'www.arbitr.ru'
    courts = {
        'OKRUG': r'http://www.arbitr.ru/as/okrug/',
        'APPEL': r'http://www.arbitr.ru/as/appeal/',
        'SUBJ': r'http://www.arbitr.ru/as/subj/',
    }

    def __init__(self):
        self.refs = dict()

    def _get_request(self, url, params={}):
        response = requests.get(url, params=params, verify=True)
        return response

    def _create_html_element(self, response):
        html_element = fromstring(response.content.decode('cp1251'))
        return html_element

    def _parse_refs(self):
        for court in self.courts.keys():
            html_element = self._create_html_element(
                self._get_request(self.courts[court])
            )
            self.refs[court] = html_element.xpath('//table//a[@class="zag21"]/@href')

    def _parse_company(self, html_element, url):
        comp_name = html_element.xpath('//h1[@class="as_header"]/text()')
        try:
            comp_name = comp_name[0]
        except IndexError:
            pass
        pattern = re.compile(r'\d{6}')
        data = html_element.xpath('//td/text()')
        address = str()
        index = 0
        for elem in data:
            try:
                if re.search(pattern, elem).group(0) is not None:
                    address = elem
                    break
            except AttributeError:
                pass
            index += 1
        address += data[index + 1]
        return [url, comp_name, address]

    def run(self):
        self._parse_refs()
        companies = []
        for court, refs in self.refs.items():
            for ref in refs:
                full_ref = urljoin(self.courts[court], ref)
                try:
                    response = self._get_request(full_ref)
                    html_element = self._create_html_element(response)
                    comp_profile = self._parse_company(html_element, full_ref)
                    companies.append(comp_profile)
                except ConnectionError:
                    pass
        self._save(companies)

    def _save(self, data):
        columns = ['URL', 'Company', 'Address']
        df = pd.DataFrame(data=data,
                          columns=columns)
        df.to_excel('Courts.xlsx')


scrapper = Courts_scrapper()
scrapper.run()



