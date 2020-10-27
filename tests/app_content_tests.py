import base64
import json
import os
import re
import shutil
import sys
import unittest
sys.path.append('../ios_data_client')
from ios_data_client import *


url = 'https://itunes.apple.com/us/genre/ios-health-fitness/id6013?mt=8'
category = 'Health-Fitness'
app = 'https://apps.apple.com/us/app/sweatcoin/id971023427'
appid = re.findall(r'\d+', app)[0]

class BasicTests(unittest.TestCase):
 
###############
#### tests ####
###############

    def test_get_raw(self):
        ''' Test for getting raw json for a give app.
        '''
        health_app = GetAppContent()
        apd = health_app.get_raw_app_json(appid)
        assert len(apd) != 0
        assert 'results' in apd.keys()
        assert 'description' in apd['results'][0].keys()

    def test_get_app_json(self):
        ''' Test for getting app info json.
        '''
        health_app = GetAppContent()
        apd = health_app.get_app_json(appid)
        assert len(apd) != 0
        assert 'results' in apd.keys()

    def test_get_images(self):
        ''' Test for getting app images.
        '''
        health_app = GetAppContent()
        apd = health_app.get_raw_app_json(appid)
        img = apd['results'][0]['screenshotUrls'][0]
        health_app.get_images(img, './img', 1)
        assert len(os.listdir('./img')) != 0
        shutil.rmtree("./img")

    def test_get_sel_json(self):
        ''' Test for getting raw json for a give app.
        '''
        health_app = GetAppContent()
        health_app.get_selected_apps_json(category, [app])
        with open(f"./{category}/{appid}.json") as f:
            apd = json.load(f)
        assert len(apd) != 0
        assert 'app_summary' in apd.keys()
        assert 'description' in apd['results'].keys()
        shutil.rmtree(f"./{category}")

    def test_get_img_json(self):
        ''' Test for getting json and images for a give app.
        '''
        health_app = GetAppContent()
        health_app.get_images_json(category, [app])
        assert appid in os.listdir('.')
        assert len(os.listdir(f"./{appid}")) != 0
        assert len(os.listdir(f"./{appid}/")) != 0
        shutil.rmtree(f"./{appid}")       

    def test_summary(self):
        ''' Test for summarizing app description.
        '''
        health_app = GetAppContent()
        apd = health_app.get_raw_app_json(appid)
        desc = apd['results'][0]['description']
        summary = health_app.text_summary(desc)
        assert len(summary) < len(desc)

if __name__ == "__main__":
    unittest.main()