from store_countries import CountryCodes
from store_info import GetStoreInfo
from store_countries import CountryCodes
from store_data import StoreAppData
from store import Store

class IosDataClient:

    def __init__(self, **kwargs):
        self.genre = kwargs.get('genre', None)
        self.country = kwargs.get('country', None)
        self.urlstart = kwargs.get('urlstart', None)
        self.countries = CountryCodes()
        self.store = Store(**kwargs)


if __name__ == '__main__':
    client = IosDataClient(genre='Sports', country='Australia')
    client.countries.countries
    client.store.info.get_genres()
    print(client.store.info.genres)
    client.store.get_top_apps(top=2)