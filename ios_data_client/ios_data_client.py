from .store_countries import CountryCodes
from .store_info import GetStoreInfo
from .store_countries import CountryCodes
from .store_data import StoreAppData
from .store import Store

class IosDataClient:

    def __init__(self, **kwargs):
        self.countries = CountryCodes()
        self.store = Store()

