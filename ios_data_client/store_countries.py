"""
ios_data_client.store_countries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains code for managing the country specific information
needed when looking at the app store.
"""

from pathlib import Path
import pickle
import pprint

project_base = Path(__file__).resolve().parent.parent
store_data = project_base.joinpath('ios_data_client')

class CountryCodes:
    '''
    Simple class for loading country information.
    '''

    def __init__(self):
        self.codes = self.load_codes()

    def load_codes(self):
        '''
        Method for loading country codes from pickle file.
        '''
        with open(store_data.joinpath('country_codes.pickle'), 'rb') as f:
            return pickle.load(f)

    @property
    def countries(self):
        '''
        Property to list countries and codes.
        '''
        pprint.pprint(self.codes)
