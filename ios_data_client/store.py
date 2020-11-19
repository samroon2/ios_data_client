'''
ios_data_client.store
~~~~~~~~~~~~~~~~~~~~~
This module contains code for interacting with the ios store.
'''

import bs4 as bs
import requests
from .exceptions import UndefinedGenre
from .store_info import GetStoreInfo
from .store_countries import CountryCodes
from .store_data import StoreAppData

class Store(GetStoreInfo, StoreAppData, CountryCodes):
    '''
    Class for scraping app information from the ios app store.
    GetStoreInfo to get app info from the store -> driver for app id's/lists to obtain
    StoreAppData -> get app description, art etc, items present in the app store.
    UserReviews -> get reviews
    :param urlstart: Staring url for data.
    :type urlstart: str
    ''' 
    def __init__(self, **kwargs):
        super(Store, self).__init__()
        self.country = kwargs.get('country', 'United States')
        self.country_codes = CountryCodes()
        self.country_code = self.country_codes.codes[self.country]['alpha_2']
        self.info = GetStoreInfo(country_code=self.country_code)
        self.data = StoreAppData()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}

    @staticmethod
    def get_id(app_url: str) -> str:
        ''' 
        Simple static method to return appid.
        :param app_url: appstore url for a specific app.
        :type app_url: str
        '''
        return app_url.split('id')[-1].split('?')[0]
        
    def get_top_apps(self, genre: str, top=100, json_only=False):
        '''
        Method to obtain popular listed apps.
        :param genre: Desired genre.
        :type genre: str
        :param top: Number of top apps to return.
        :type top: int
        :param json_only: Return only json.
        :type json_only: bool
        '''
        if genre not in self.genres:
            raise UndefinedGenre(genre, self.genres)
        elif not json_only:
            self.get_images_json(genre, [title for title in self.get_popular_apps(genre)][0][:top if top else None])
        else:
            self.get_selected_apps_json(genre, [title for title in self.get_popular_apps(genre)][0][:top if top else None])

    def get_all_apps(self, genre: str, n_letters=1, n_pages=1, n_apps=1):
        '''
        Works through the alpha list, gets pages/letter and retrieves app info.
        :param genre: Desired genre.
        :type genre: str
        :param n_letters: Number of letters to return.
        :type n_letters: int
        :param n_pages: Number of pages to iterate through for each letter.
        :type n_pages: int
        :param n_apps: Number of apps to return per letter per page.
        :type n_apps: int
        '''
        if genre not in self.genres:
            raise UndefinedGenre(genre, self.genres)
        self.get_alpha_lists()
        for link in list(set(self.alpha))[:n_letters]:
            self.get_page_list(link)
            for lin in list(set(self.pages))[:n_pages]:
                res = requests.get(lin, headers=self.headers)
                res.raise_for_status()
                noStarchSoup = bs.BeautifulSoup(res.text, "lxml")
                for url in noStarchSoup.find_all('div', {"class":"grid3-column"}):
                    self.get_images_json(genre, [ul.get('href') for ul in url.find_all('a')][:n_apps])
