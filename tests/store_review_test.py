import base64
import json
import os
import re
import shutil
import sys
import unittest
sys.path.append('../ios_data_client')
from ios_data_client.store_reviews import AppReviews
from ios_data_client.exceptions import UndefinedGenre

appid = '971023427'

class BasicTests(unittest.TestCase):

    def test_write(self):
        '''
        Test for write to json.
        '''
        d = {'test':1}
        reviews = AppReviews()
        reviews.write_to_json('test', d)
        assert 'test.json' in os.listdir('.')
        with open(f'test.json') as f:
            d = json.load(f)
        assert d['test'] == 1
        os.remove('test.json')

    def test_get_review(self):
        token = os.getenv('IOSTOKEN')
        reviews = AppReviews()
        req = reviews.get_auth_reviews(appid, token, 0)
        assert req.status_code == 200
        assert req.json()['data']

    def test_get_app(self):
        token = os.getenv('IOSTOKEN')
        reviews = AppReviews()
        reviews.get_all_auth_revs(appid, token, limit=10)
        assert appid in os.listdir('.')
        assert len(os.listdir(f'{appid}/reviews')) == 2
        with open(f'{appid}/reviews/reviews_page_0.json') as f:
            d = json.load(f)
        assert d['data']
        shutil.rmtree(appid)

    def test_get_batch(self):
        token = os.getenv('IOSTOKEN')
        reviews = AppReviews()
        apps = [appid, '336381998', '680520990']
        reviews.get_all_auth_revs_batch(apps, token, limit=10)
        assert all([x in os.listdir('.') for x in apps])
        assert len(os.listdir(f'{appid}/reviews')) == 2
        with open(f'{appid}/reviews/reviews_page_0.json') as f:
            d = json.load(f)
        assert d['data']
        [shutil.rmtree(x) for x in apps]

if __name__ == '__main__':
    unittest.main()
