[![Build Status](https://travis-ci.org/samroon2/ios_data_client.svg?branch=main)](https://travis-ci.org/samroon2/ios_data_client)
# ios_data_client
Client for ios app data.

ios_data_client is a python library for iterating/accessing the ios store apis to obtain data about apps featured in the ios store.

## Getting Started.

```bash
>>> from ios_data_client import IosDataClient
>>> client = IosDataClient(country='United States')
```
### Get App Meta Data, Including; Description, Genres, Artwork, Screenshots etc.
Package provides an easy Python client to get app data from the store. This includes the following;
-  App meta data; genre, price, description, supported devices etc.
-  App artwork and screenshots.
-  App reviews.

### Get App Meta Data
 ```bash
>>> from ios_data_client import IosDataClient
>>> client = IosDataClient(country='United States')
>>> client.store.get_app_json('1477376905')
{'resultCount': 1,
 'results': {'isGameCenterEnabled': False,
  'screenshotUrls':
  ..
  'averageUserRating': 4.79817,
  'trackViewUrl': 'https://apps.apple.com/us/app/github/id1477376905?uo=4',
  'trackContentRating': '4+',
  'bundleId': 'com.github.stormbreaker.prod',
  'trackId': 1477376905,
  'trackName': 'GitHub',
  'genres': ['Developer Tools', 'Productivity'],
  'formattedPrice': 'Free',
  ..
  'description': 'There’s a lot you can do on GitHub that doesn’t require a complex development environment – like sharing feedback on a design discussion, or reviewing a few lines of code. GitHub for iOS lets you move work forward wherever you are. Stay in touch with your team, triage issues, and even merge, right from the app. We’re making these tasks easy for you to perform, no matter where you work, with a beautifully native experience.\n\nYou can use GitHub for iOS to:\n\n• Browse your latest notifications\n• Read, react, and reply to Issues and Pull Requests\n• Review and merge Pull Requests\n• Organize Issues with labels, assignees, projects, and more\n• Browse your files and code\n• Discover new and trending repositories\n\n———\n\nTerms of Service: https://docs.github.com/en/github/site-policy/github-terms-of-service\nPrivacy Policy: https://docs.github.com/en/github/site-policy/github-privacy-statement',
  ..
 'app_id': 1477376905,
 'app_name': 'GitHub',
 'app_summary': 'GitHub for iOS lets you move work forward wherever you are..Stay in touch with your team, triage issues, and even merge, right from the app.'}
```

### Get Selected Apps
Get selected data for selected apps.
#### Get JSON for Selected Apps
```bash
>>> from ios_data_client import IosDataClient
>>> client = IosDataClient(country='United States')
>>> client.store.get_selected_apps_json('Developer Tools', ['1477376905', '1459215293'])
>>> import os
>>> os.listdir()
['Developer Tools']
>>> os.listdir('Developer Tools')
['1477376905.json', '1459215293.json']
```
#### Get JSON + Images/Artwork
```bash
>>> from ios_data_client import IosDataClient
>>> client = IosDataClient(country='United States')
>>> client.store.get_images_json('Developer Tools', ['1477376905', '1459215293'])
>>> import os
>>> os.listdir()
['Developer Tools']
>>> os.listdir('Developer Tools')
['1459215293', '1477376905']
>>> os.listdir('Developer Tools/1477376905')
['1477376905.json', 'artwork', 'ipadScreenshot', 'screenshots']
>>> os.listdir('Developer Tools/1477376905/screenshots')
['0_392x696bb.png', '3_392x696bb.png', '1_392x696bb.png', '2_392x696bb.png']
```
### Get top Apps of a Given Genre
```bash
>>> from ios_data_client import IosDataClient
>>> client = IosDataClient(country='United States')
>>> client.store.get_top_apps('Developer Tools', top=1, json_only=False)
>>> import os
>>> os.listdir()
['Developer Tools']
>>> os.listdir('Developer Tools')
['1517331914']
>>> os.listdir('Developer Tools/1517331914')
['1517331914.json', 'artwork', 'ipadScreenshot', 'screenshots']
```
### Get all Apps of a Given Genre
```bash
>>> from ios_data_client import IosDataClient
>>> client = IosDataClient(country='United States')
>>> client.store.get_all_apps('Developer Tools', n_letters=1, n_pages=1, n_apps=1)
>>> import os
>>> os.listdir()
['Developer Tools']
>>> os.listdir('Developer Tools')
['864038041']
>>> os.listdir('Developer Tools/864038041')
['864038041.json', 'artwork', 'ipadScreenshot', 'screenshots']
```
### Get App Reviews
#### Get Reviews for a Single App
```bash
>>> from ios_data_client import IosDataClient
>>> client = IosDataClient(country='United States')
>>> import os
>>> os.listdir()
['Developer Tools']
>>> os.listdir('Developer Tools')
['864038041']
>>> client.reviews.get_all_auth_revs(os.listdir('Developer Tools')[0], os.environ['IOSTOKEN'], start=0, limit=10)
100%|████████████████████████████████████████████████████████████████████████████████████| 10/10 [00:09<00:00,  1.09 Reviews/s]
>>> os.listdir('864038041')
['reviews']
>>> os.listdir('864038041/reviews')
['reviews_page_0.json', 'reviews_page_10.json']
```
####  Get Reviews for Multiple Apps
__Note:__ this should be done ethically, do not abuse this!!! Submit batches of ~5 apps at a time, limit the number of reviews, sleep in between batches or you will get blocked by the host!
```bash
>>> from ios_data_client import IosDataClient
>>> client = IosDataClient(country='United States')
>>> client.reviews.get_all_auth_revs_batch(['1483790257', '1477376905'], os.environ['IOSTOKEN'], limit=100, alt_headers=False, tqdm_disable=False)
100%|█████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:10<00:00, 10.01Reviews/s]
100%|█████████████████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:11<00:00, 9.09Reviews/s]
>>> os.listdir('1483790257')
['reviews']
>>> os.listdir('1483790257/reviews')
['reviews_page_40.json', 'reviews_page_90.json', 'reviews_page_70.json', 'reviews_page_60.json', 'reviews_page_30.json', 'reviews_page_20.json', 'reviews_page_80.json', 'reviews_page_0.json', 'reviews_page_50.json', 'reviews_page_10.json']
>>> import json
>>> with open(f'1483790257/reviews/reviews_page_40.json') as f:
...     d = json.load(f)
>>> d
{'data': [{'attributes': {'date': '2020-01-16T00:46:33Z',
                          'isEdited': False,
                          'rating': 4,
                          'review': 'All I wanted was an editor for plain text '
                                    'and so far so good',
                          'title': 'Edits plain text'},
           'id': '5408564353',
           'type': 'user-reviews'},
....
}
```