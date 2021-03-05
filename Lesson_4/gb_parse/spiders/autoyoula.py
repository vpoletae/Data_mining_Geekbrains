import scrapy
import pymongo
import re

class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['http://auto.youla.ru/']

    _css_selectors = {
        'brands': ".TransportMainFilters_brandsList__2tIkv "
                ".ColumnItemList_container__5gTrc "
                "a.blackLink",
        'pagination': "a.Paginator_button__u1e7D",
        'car': 'SerpSnippet_titleWrapper__38bZM a.SerpSnippet_name__3_y7m',

        'name': 'AdvertCard_advertTitle__1S1Ak::text',
        'price': 'div.AdvertCard_price__3dDCr::text',
        'photos': 'figure.PhotoGallery_photo__36e_r img',
        'features': 'AdvertCard_specs__2FEHc .AdvertSpecs_row__ljPcX',
        'feat_name': '.AdvertSpecs_label__2JHnS::text',
        'feat_value_1': '.AdvertSpecs_data__xK2Qx::text',
        'feat_value_2': '.AdvertSpecs_data__xK2Qx a::text',
        'description': 'AdvertCard_descriptionInner__Knuri::text',
        'author': 'SellerInfo_name__3Iz2N::text',
        'phone': 'PopupPhoneNumber_number__1hybY::text',
    }

    def __init__(self):
        self.db_client = pymongo.MongoClient('mongodb://localhost:27017/')
        self.db = self.db_client['gb_data_mining']
        self.collection = self.db['youla_cars']

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            link = a.attrib.get('href')
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def parse(self, response, *args, **kwargs):
        yield from self._get_follow(response,
                                    self._css_selectors['brands'],
                                    self.brand_parse,
                                    hello='moto')

    def brand_parse(self, response, *args, **kwargs):
        yield from self._get_follow(response,
                                    self._css_selectors['pagination'],
                                    self.brand_parse,
                                    )

        yield from self._get_follow(response,
                                    self._css_selectors['car'],
                                    self.car_parse,
                                    )

    def get_author_id(self, response):
        marker = 'window.transitState = decodeURIComponent'
        for script in response.css('script'):
            try:
                if marker in script.css('::text').extract_first():
                    re_pattern = re.compile(r'youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar')
                    result = re.findall(re_pattern, script.css('::text').extract_first())
                    return response.urljoin(f'/user/{result[0]}') if result else None
            except TypeError:
                pass

    def car_parse(self, response):
        try: # create a separate data query
            data = {
                'name': response.css(self._css_selectors['name']).get(),
                'price': float(response.css(self._css_selectors['price']).get().replace('\u2009', '')),
                'photos': [photo.attrib.get('src') for photo in
                        response.css(self._css_selectors['photos'])],
                'features': [{'name': feat.css(self._css_selectors['feat_name']).extract_first(),
                             'value': feat.css(self._css_selectors['feat_value_1']).extract_first() or
                             feat.css(self._css_selectors['feat_value_2']).extract_first()} for
                             feat in response.css(self._css_selectors['features'])],
                'description': response.css(self._css_selectors['description']).extract_first(),
                'author': self.get_author_id(response),
            }
            self.collection.insert_one(data)
        except (ValueError, AttributeError):
            pass