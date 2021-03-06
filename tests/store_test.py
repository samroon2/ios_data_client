import base64
import json
import os
import re
import shutil
import sys
import unittest
sys.path.append('../ios_data_client')
from ios_data_client import Store
from ios_data_client.exceptions import UndefinedGenre


url = 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8'
genre = 'Health & Fitness'
app = 'https://apps.apple.com/us/app/sweatcoin/id971023427'
appid = re.findall(r'\d+', app)[0]

class BasicTests(unittest.TestCase):

    def test_popular_apps_info(self):
        '''
        Test for popular app method.
        '''
        health = Store()
        assert len([x for x in health.info.get_popular_apps(genre)]) != 0

    def test_get_genres(self):
        '''
        Test for getting genres from the app store.
        '''
        health = Store()
        health.info.get_genres()
        assert len(health.info.genres) != 0

    def test_alpha_list(self):
        '''
        Test for determining the alpha list in the app store.
        '''
        health = Store()
        health.info.get_alpha_lists()
        assert len(health.info.alpha) != 0

    def test_page_list(self):
        '''
        Test for determining the alpha list in the app store.
        '''
        health = Store()
        health.info.get_alpha_lists()
        health.info.get_page_list(health.info.alpha[0])
        assert len(health.info.pages) != 0

    def test_get_raw(self):
        ''' 
        Test for getting raw json for a give app.
        '''
        health_app = Store()
        apd = health_app.data.get_raw_app_json(appid)
        assert len(apd) != 0
        assert 'results' in apd.keys()
        assert 'description' in apd['results'][0].keys()

    def test_get_app_json(self):
        ''' 
        Test for getting app info json.
        '''
        health_app = Store()
        apd = health_app.data.get_app_json(appid)
        assert len(apd) != 0
        assert 'results' in apd.keys()

    def test_get_images(self):
        ''' 
        Test for getting app images.
        '''
        health_app = Store()
        apd = health_app.data.get_raw_app_json(appid)
        img = apd['results'][0]['screenshotUrls'][0]
        health_app.data.get_images(img, './img', 1)
        assert len(os.listdir('./img')) != 0
        shutil.rmtree("./img")

    def test_get_sel_json(self):
        ''' 
        Test for getting raw json for a give app.
        '''
        health_app = Store()
        health_app.data.get_selected_apps_json(genre, [app])
        with open(f"./{genre}/{appid}.json") as f:
            apd = json.load(f)
        assert len(apd) != 0
        assert 'app_summary' in apd.keys()
        assert 'description' in apd['results'].keys()
        shutil.rmtree(f"./{genre}")

    def test_get_img_json(self):
        ''' 
        Test for getting json and images for a give app.
        '''
        health_app = Store()
        health_app.data.get_images_json(genre, [app])
        assert appid in os.listdir(f'{genre}')
        assert len(os.listdir(f"{genre}/{appid}")) != 0
        assert len(os.listdir(f"{genre}/{appid}/")) != 0
        shutil.rmtree(f"{genre}/{appid}")

    def test_summary(self):
        ''' 
        Test for summarizing app description.
        '''
        health_app = Store()
        apd = health_app.data.get_raw_app_json(appid)
        desc = apd['results'][0]['description']
        summary = health_app.data.text_summary(desc)
        assert len(summary) < len(desc)

    def test_store_wrong_genre(self):
        ''' 
        Test for summarizing app description.
        '''
        health_app = Store()
        try:
            health_app.get_top_apps('Health')
        except UndefinedGenre as g:
            print(g)

if __name__ == "__main__":
    unittest.main()
