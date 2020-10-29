import base64
import json
import os
import re
import shutil
import sys
import unittest
sys.path.append('../ios_data_client/ios_data_client')
import os
print(os.listdir())
from ios_data_client import IosDataClient
from unittest.mock import patch


url = 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8'
genre = 'Health & Fitness'
category = 'Health-Fitness'

class BasicTests(unittest.TestCase):
 
###############
#### tests ####
###############

    def test_get_popular_apps(self):
        '''Test to get popular apps.
        '''
        dats = IosDataClient(genre=genre, country="United States")#urlstart=url
        print(dats.urlstart)
        dats.get_top_apps(top=5)
        downloads = [x for x in os.listdir('.') if '.py' not in x]
        assert len(downloads) > 0
        # [shutil.rmtree(f"./{x}") for x in downloads]

    def test_get_selected_app(self):
        '''Test for retrieving data for a seleted app.
        '''
        dats = IosDataClient(genre=genre, country="United States")
        print(dats.genres)

    def test_get_all_apps(self):
        '''Test for downloading all apps.
        '''
        dats = IosDataClient(genre=genre, country="United States")
        dats.store.get_all_apps(n_letters=1, n_pages=1)
        downloads = [x for x in os.listdir('.') if '.py' not in x]
        assert len(downloads) > 0
        # [shutil.rmtree(f"./{x}") for x in downloads]

if __name__ == "__main__":
    unittest.main()