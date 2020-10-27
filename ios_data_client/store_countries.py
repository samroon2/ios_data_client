from pathlib import Path
import pickle
import pprint

project_base = Path(__file__).resolve().parent.parent

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
        with open('country_codes.pickle', 'rb') as f:
            return pickle.load(f)

    @property
    def countries(self):
        '''
        Property to list countries and codes.
        '''
        pprint.pprint(self.codes)