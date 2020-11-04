import bs4 as bs
import datetime
import json
import requests
import os
import time
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer


class StoreAppData:
    '''Class for extracting data for apps.
    '''

    def get_raw_app_json(self, appid: str):
        '''
        Retrieve app data.
        :param appid: ID of ios application.
        :type appid: str
        '''
        lookupurl = "https://itunes.apple.com/lookup?id={}".format(appid)
        resp = requests.get(lookupurl)
        data = resp.json()
        return data

    def get_images(self, picurl: str, dirr: str, indexx: int):
        '''
        Method for downloading app images.
        :param picurl: url of image to download.
        :type picurl: str
        :param dirr: directory to store image.
        :type dirr: str
        :param indexx: index of image (used for naming)
        :type indexx: int
        '''
        os.makedirs (dirr) if not os.path.isdir(dirr) else False
        fn = dirr + '/' + str(f'{indexx}_') + picurl.split("/")[-1]
        r = requests.get(picurl, stream=True)
        f = open(fn, 'wb')
        for chunk in r.iter_content(chunk_size=512 * 1024):
            if chunk:
                f.write(chunk)
        f.close()

    def get_selected_apps_json(self, genre: str, selectedtitles: list):
        '''
        Get data for a given genre/list of selcted apps.
        :param genre: App store genre to be collected.
        :type genre: str
        :param selectedtitles: List of selected titles urls.
        :type selectedtitles: list
        '''
        if not os.path.exists(f'./{genre}'):
            os.makedirs(f'./{genre}')
        for app in selectedtitles:
            appid = app.split('id')[-1].split('?')[0]
            appjson = self.get_app_json(appid)
            with open(f'./{genre}/{str(appid)}.json', "w") as outfile:
                json.dump(appjson, outfile)
            time.sleep(1)

    def get_images_json(self, genre: str, selectedtitles: list):
        '''
        Method that retrieves images and json for apps.
        :param genre: App store genre to be collected.
        :type genre: str
        :param apps: List of app urls to get.
        :type apps: list
        '''
        os.makedirs(genre) if genre not in os.listdir('.') else False
        for app in selectedtitles:
            appid = app.split('id')[-1].split('?')[0]
            basepath = f'./{genre}/{str(appid)}'
            os.makedirs(basepath) # Handle FileExistsError
            os.makedirs(f'{basepath}/screenshots')
            os.makedirs(f'{basepath}/ipadScreenshot')
            os.makedirs(f'{basepath}/artwork')
            appjson = self.get_raw_app_json(appid)
            [self.get_images(x, f'{basepath}/screenshots', n) for n, x in enumerate(appjson['results'][0]['screenshotUrls'])]
            [self.get_images(x, f'{basepath}/ipadScreenshot', n) for n, x in enumerate(appjson['results'][0]['ipadScreenshotUrls'])]
            self.get_images(appjson['results'][0]['artworkUrl512'], f'{basepath}/artwork', 0)
            with open(f'{basepath}/{str(appid)}.json', "w") as outfile:
                json.dump(appjson, outfile)
            time.sleep(1)

    def get_app_json(self, appid: str):
        '''
        Method for obtaining app details in json, takes appid which is apples app specific ID.
        :param appid: ID of app.
        :type appid: str
        :returns data: Formated json.
        '''
        try:
            data = self.get_raw_app_json(appid)
            data['results'] = data['results'][0]
            data['date_obtained'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data['lookup_url'] = "https://itunes.apple.com/lookup?id={}".format(appid)
            data['app_id'] = data['results']['trackId']
            data['app_name'] = data['results']['trackName']
            data['app_summary'] = str(self.text_summary(data['results']['description'].replace(">","")))
            #self.storejson(data)
            return data
        except Exception as e:
            print(f"failed on: {e}")   

    def text_summary(self, text: str):
        '''
        Method to provide a 2 sentence summary of the app description.
        :param text: Body of text describing app.
        :type text: str
        '''
        parser = PlaintextParser(text, Tokenizer("english"))
        stemmer = Stemmer("english")
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words("english")
        concatsent = []
        for x in summarizer(parser.document, 3):
            concatsent.append(str(x))
        concatsent.pop(0)
        return ".".join(concatsent)
