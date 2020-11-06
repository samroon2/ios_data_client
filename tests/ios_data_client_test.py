import base64
import json
import os
import re
import shutil
import sys
import unittest
sys.path.append('../ios_data_client')
import os
from ios_data_client import IosDataClient
from unittest.mock import patch

url = 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8'
genre = 'Health & Fitness'
app = 'https://apps.apple.com/us/app/sweatcoin/id971023427'
appid = re.findall(r'\d+', app)[0]

class BasicTests(unittest.TestCase):

    def test_a_get_all_apps(self):
        '''
        Test for downloading all apps.
        '''
        dats = IosDataClient(country="United States")
        dats.store.get_all_apps(genre)
        downloads = [x for x in os.listdir('.') if '.py' not in x]
        assert len(downloads) > 0

    def test_b_get_popular_apps(self):
        '''
        Test to get popular apps.
        '''
        dats = IosDataClient(country="United States")
        dats.store.get_top_apps(genre, top=5)
        downloads = [x for x in os.listdir(f'{genre}')]
        assert len(downloads) > 0
        shutil.rmtree(f"{genre}")

    def test_c_get_popular_apps_json_only(self):
        '''
        Test to get popular apps.
        '''
        dats = IosDataClient(country="United States")
        dats.store.get_top_apps(genre, top=5, json_only=True)
        downloads = [x for x in os.listdir(f'{genre}') if x.endswith('.json')]
        assert len(downloads) > 0
        shutil.rmtree(f"{genre}")

    def test_d_get_selected_app(self):
        '''
        Test for retrieving data for a seleted app.
        '''
        health_app = IosDataClient(country="United States")
        health_app.store.data.get_selected_apps_json(genre, [app])
        with open(f"./{genre}/{appid}.json") as f:
            apd = json.load(f)
        assert len(apd) != 0
        assert 'app_summary' in apd.keys()
        assert 'description' in apd['results'].keys()
        shutil.rmtree(f"./{genre}")

if __name__ == "__main__":
    unittest.main()