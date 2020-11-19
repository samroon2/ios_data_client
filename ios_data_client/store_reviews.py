'''
ios_data_client.store_reviews
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains code for obtaining app reviews from the ios store.
'''

import collections
import heapq
import json
import os
import pathlib
import random
import requests
import time
from tqdm import tqdm
from .store_countries import CountryCodes

class AppReviews:
    '''
	Retreieves reviews from the app store.
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
        self.headers_2 = {"User-Agent": 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'}
        self.sort_orders = {'most recent': 0,'most helpful': 1, 'most favorable' : 2, 'most critical':3}
        self.tqs = None

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

    def get_auth_reviews(self, appid: str, token: str, offset: int, alt_headers=False):
        '''
		Method to make http request to get reviews.
		:param appid: ID of the app.
		:type appid: str
		:param token: Bearer Token.
		:type token: str
		:param offset: Review offset.
		:type offset: int
        :param alt_headers: Use alternate headers.
		:type alt_headers: bool
		'''
		# TODO: language param.
        a = f'https://amp-api.apps.apple.com/v1/catalog/{self.countrycodealpha}/apps/{appid}/reviews?l=en-US&offset={offset}&platform=web&additionalPlatforms=appletv%2Cipad%2Ciphone%2Cmac'
        self.headers['authorization'] = f'Bearer {token}'
        self.headers_2['authorization'] = f'Bearer {token}'
        res = requests.get(a, headers=self.headers if not alt_headers else self.headers_2)
        return res

    def get_all_auth_revs(self, appid: str, token: str, start=0, limit=100):
        '''
		Method to get reviews for a single app.
		:param appid: ID of the app.
		:type appid: str
		:param token: Bearer Token.
		:type token: str
		:param start: Number of reviews to skip.
		:type start: int
		:param limit: Max number of reviews to get.
		:type limit: int
		'''
        offset = start
        os.makedirs(f'{str(appid)}/reviews') if appid not in os.listdir('.') else None
        tq = tqdm(total=limit, unit='Reviews')
        retry = 0
        while offset <= limit and retry < 5:
            d = self.get_auth_reviews(appid, token, offset)
            if d.status_code == 200:
                self.write_to_json(f'{appid}/reviews/reviews_page_{offset}', d.json())
                offset += 10
                time.sleep(random.randint(2, 20))
                tq.update(10)
                retry = 0
            elif d.status_code == 429:
                time.sleep(random.randint(2, 30))
                retry += 1
            else:
                retry += 1
        
    def get_all_auth_revs_batch(self, apps: list, token: str, limit=100, alt_headers=False, tqdm_disable=False):
        '''	
		Method to get reviews for a single app, built to be slow/respectful.
		:param appid: ID of the app.
		:type appid: str
		:param token: Bearer Token.
		:type token: str
		:param limit: Max number of reviews to obtain.
		:type limit: int
        :param alt_headers: Use alternate headers.
		:type alt_headers: bool
        :param tqdm_disable: Disable tqdm visualization.
		:type tqdm_disable: bool
		'''
        heap = []
        if not self.tqs:
            self.tqs = {i:tqdm(total=limit, unit='Reviews', disable=tqdm_disable) for i in range(len(apps))}
        tqdm._instances.clear()
        for i, app in enumerate(apps):
            os.makedirs(f'{str(app)}/reviews') if app not in os.listdir('.') else None
            heap.append((0, 0, 0, app, i))
        heapq.heapify(heap)
        reqs = 0
        history = collections.deque([])
        while heap:
            last_ran, offset, retries, app, idx = heapq.heappop(heap)
            if len(history) > 100:
                history.popleft()
            s_term = list(history)[-10:].count(429)/10
            if offset <= limit:
                if reqs-last_ran < 2:
                    time.sleep(1)
                if s_term > 0.75:
                    time.sleep(5)
                try:
                    d = self.get_auth_reviews(app, token, offset, alt_headers=alt_headers)
                except Exception:
                    if retries < 20:
                        alt_headers = not alt_headers
                        heapq.heappush(heap, (reqs+20, offset, retries + 1, app, idx))
                        reqs += 1
                    continue
                if d.status_code == 200:
                    self.write_to_json(f'{app}/reviews/reviews_page_{offset}', d.json())
                    heapq.heappush(heap, (reqs, offset + 10, 0, app, idx))
                    reqs += 1
                    self.tqs[idx].update(10)
                    history.append(200)
                elif d.status_code == 429:
                    if retries < 10:
                        heapq.heappush(heap, (reqs+10, offset, retries + 1, app, idx))
                        reqs += 1
                        history.append(429)
                elif retries < 3:
                    heapq.heappush(heap, (reqs, offset, retries + 1, app, idx))
                    reqs += 1
