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

### Get all Apps

### Get App Reviews