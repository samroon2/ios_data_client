
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

    def self_check(self):
        '''
        Method for ensuring required information is present for requests.
        '''
        if not self.urlstart or (not self.genre and not self.country):
            if not self.genre:
                while self.genre not in self.info.genres:
                    self.genre = input(f'Please enter a genre or starting URL {self.info.genres}')
            elif self.genre not in self.info.genres:
                while self.genre not in self.info.genres:
                    self.genre = input(f'Please enter a genre or starting URL {self.info.genres}')
            self.urlstart = self.info.genres[self.genre]

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
        '''
        if genre not in self.genres:
            raise UndefinedGenre(genre, self.genres) # return 'No Such Genre' # Create exception for this.
        # self.self_check()
        if not json_only:
            self.get_images_json(genre, [title for title in self.popular_titles[:top if top else len(self.popular_titles)]])
        else:
            self.get_selected_apps_json(genre, [title for title in self.get_popular_apps(genre)][0][:top if top else None])

    def get_all_apps(self, genre: str, n_letters=1, n_pages=1, n_apps=1):
        '''
        Works through the alpha list, gets pages/letter and retrieves app info.
        '''
        # self.self_check()
        self.get_alpha_lists()
        for link in list(set(self.alpha))[:n_letters]:
            self.get_page_list(link)
            for lin in list(set(self.pages))[:n_pages]:
                res = requests.get(lin, headers=self.headers)
                res.raise_for_status()
                noStarchSoup = bs.BeautifulSoup(res.text, "lxml")
                for url in noStarchSoup.find_all('div', {"class":"grid3-column"}):
                    self.get_images_json(genre, [ul.get('href') for ul in url.find_all('a')][:n_apps])
