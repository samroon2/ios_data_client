import base64
import json
import os
import re
import shutil
import sys
import unittest
sys.path.append('../ios_data_client/ios_data_client')
import os
from ios_data_client import IosDataClient
from unittest.mock import patch


url = 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8'
genre = 'Health & Fitness'
category = 'Health-Fitness'

class BasicTests(unittest.TestCase):
 
###############
#### tests ####
###############


    def test_a_get_all_apps(self):
        '''
        Test for downloading all apps.
        '''
        dats = IosDataClient(genre=genre, country="United States")
        dats.store.get_all_apps(n_letters=1, n_pages=1)
        downloads = [x for x in os.listdir('.') if '.py' not in x]
        assert len(downloads) > 0

    def test_b_get_popular_apps(self):
        '''
        Test to get popular apps.
        '''
        dats = IosDataClient(genre=genre, country="United States")
        print(dats.urlstart)
        dats.store.get_top_apps(top=5)
        downloads = [x for x in os.listdir(f'{genre}')]
        assert len(downloads) > 0
        shutil.rmtree(f"{genre}")

    def test_c_get_popular_apps_json_only(self):
        '''
        Test to get popular apps.
        '''
        dats = IosDataClient(genre=genre, country="United States")
        print(dats.urlstart)
        dats.store.get_top_apps(top=5, json_only=True)
        downloads = [x for x in os.listdir(f'{genre}') if x.endswith('.json')]
        assert len(downloads) > 0
        shutil.rmtree(f"{genre}")

    def test_d_get_selected_app(self):
        '''
        Test for retrieving data for a seleted app.
        '''
        dats = IosDataClient(genre=genre, country="United States")
        print(dats.store.genres)

if __name__ == "__main__":
    unittest.main()