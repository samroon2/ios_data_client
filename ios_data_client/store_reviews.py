'''
ios_data_client.store_reviews
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains code for obtaining app reviews from the ios store.
'''

import heapq
import json
import os
import pathlib
import random
import requests
import time
from .store_countries import CountryCodes

class AppReviews:
    '''
	Retreieves new reviews from the app store.
    :param country: Country origin for the reviews.
	:type country: str
    '''

    def __init__(self, country='United States'):
        self.country = country
        self.countries = CountryCodes()
        self.countrycode = self.countries.codes[self.country]['apple_code']
        self.countrycodealpha = self.countries.codes[self.country]['alpha_2']
        self.headers = {"X-Apple-Store-Front":f'{self.countrycode}',
                        "User-Agent": 'iTunes/12.4.1 (Windows; Microsoft Windows 10.0 x64 Business Edition (Build 9200); x64) AppleWebKit/7601.6016.1000.1'}
        self.sort_orders = {'most recent': 0,'most helpful': 1, 'most favorable' : 2, 'most critical':3}

    def write_to_json(self, file: str, data: dict):
        '''
		Method for writing reviews to json.
		:param file: File name to write to.
		:type file: str
		:param data: Data to be written.
		:type data: dict
		'''
        with open(f'{file}.json', 'w') as outfile:
            json.dump(data, outfile)

    def get_auth_reviews(self, appid: str, token: str, offset: int):
        '''
		Method to make http request to get reviews.
		:param appid: ID of the app.
		:type appid: str
		:param token: Bearer Token.
		:type token: str
		:param offset: Review offset.
		:type offset: int
		'''
		# TODO: language param.
        a = f'https://amp-api.apps.apple.com/v1/catalog/{self.countrycodealpha}/apps/{appid}/reviews?l=en-US&offset={offset}&platform=web&additionalPlatforms=appletv%2Cipad%2Ciphone%2Cmac'
        # headers = {"User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
        #           ,'authorization': f'Bearer {token}'}
        self.headers['authorization'] = f'Bearer {token}'
        res = requests.get(a, headers=self.headers)
        print(res)
        return res

    def get_all_auth_revs(self, appid: str, token: str, start=0, limit=100):
        '''
		Method to get reviews for a single app.
		:param appid: ID of the app.
		:type appid: str
		:param token: Bearer Token.
		:type token: str
		:param offset: Review offset.
		:type offset: int
		'''
        offset = start
        os.makedirs(f'{str(appid)}/reviews') if appid not in os.listdir('.') else None
        retry = 0
        while offset <= limit and retry < 5:
            d = self.get_auth_reviews(appid, token, offset)
            print(offset)
            if d.status_code == 200:
                self.write_to_json(f'{appid}/reviews/reviews_page_{offset}', d.json())
                offset += 10
                time.sleep(random.randint(2, 20))
                retry = 0
            elif d.status_code == 429:
                time.sleep(random.randint(2, 30))
                retry += 1
            else:
                retry += 1
        
    def get_all_auth_revs_batch(self, apps: list, token: str, limit=100):
        '''	
		Method to get reviews for a single app.
		:param appid: ID of the app.
		:type appid: str
		:param token: Bearer Token.
		:type token: str
		:param limit: Max number of reviews to obtain.
		:type limit: int
		'''
        heap = []
        for app in apps:
            os.makedirs(f'{str(app)}/reviews') if app not in os.listdir('.') else None
            heap.append((0, 0, 0, app))
        heapq.heapify(heap)
        reqs = 0
        while heap:
            last_ran, offset, retrys, app = heapq.heappop(heap)
            if offset <= limit:
                if reqs-last_ran < 2:
                    time.sleep(1)
                d = self.get_auth_reviews(app, token, offset)
                print(offset, app)
                if d.status_code == 200:
                    self.write_to_json(f'{app}/reviews/reviews_page_{offset}', d.json())
                    heapq.heappush(heap, (reqs, offset + 10, 0, app))
                    reqs += 1
                elif d.status_code == 429:
                    if retrys < 10:
                        heapq.heappush(heap, (reqs, offset, retrys + 1, app))
                        reqs += 1
                elif retrys < 3:
                    heapq.heappush(heap, (reqs, offset, retrys + 1, app))
                    reqs += 1
