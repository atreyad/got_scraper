
#%%
from lxml import html
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


#%%
#TODO Need to make this better... 
# def clean_data(season_num, episode_num, text):
#     main = re.search(r'EXT.(.*?)More on Genius', text, re.DOTALL).group(1)
#     main = main.strip()
#     list = main.split("\n\n")
#     my_df = pd.DataFrame({'lines':list})
#     my_df['speaker'] = my_df['lines'].str.extract("(^.*:)")
#     my_df['lines'] = my_df['lines'].str.replace("(^.*:)", '', regex=True)
#     my_df['speaker'] = my_df['speaker'].replace(np.nan, 'SCENE:')
#     my_df['speaker'] = my_df['speaker'].str.replace("(:)", '', regex=True)
#     my_df['season'] = season_num
#     my_df['episode'] = episode_num
#     appending_frame.append(my_df, ignore_index=True)
#     appending_frame = pd.concat(appending_frame, axis=1)
#     return appending_frame

#%%
seasons = [
    "https://genius.com/albums/Game-of-thrones/Season-1-scripts",
    "https://genius.com/albums/Game-of-thrones/Season-2-scripts",
    "https://genius.com/albums/Game-of-thrones/Season-3-scripts",
    "https://genius.com/albums/Game-of-thrones/Season-4-scripts",
    "https://genius.com/albums/Game-of-thrones/Season-5-scripts",
    "https://genius.com/albums/Game-of-thrones/Season-6-scripts",
    "https://genius.com/albums/Game-of-thrones/Season-7-scripts"
]
appending_frame = pd.DataFrame(columns= ['lines', 'speaker', 'season', 'episode'])
for season_num, url in enumerate(seasons, start = 1):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    ep_urls = tree.xpath("//div[contains(@class, 'chart_row')]/a/@href")
    for episode_num, ep in enumerate(ep_urls, start = 1):
        print(season_num, episode_num, ep)
        page = requests.get(ep)
        tree = BeautifulSoup(page.content)
        text = tree.get_text()
        text = text.replace("-", '')
        #TODO lowercase the text for all seasons
        if season_num ==1:
            text = text.lower()
            test = re.search(r'thrones-(.*?)-annotated', str(ep)).group(1)
            test = test.replace("-", ' ')
            try:
                main = re.search(r'{} lyrics(.*?)more on genius'.format(test), text, re.DOTALL).group(1)
            except AttributeError:
                test = test.rsplit(' ',1)[1]
                main = re.search(r'{} lyrics(.*?)more on genius'.format(test), text, re.DOTALL).group(1)
        else:
            try:
                print("Try Script Lyrics")
                main = re.search(r'Script[\)]* Lyrics(.*?)More on Genius', text, re.DOTALL).group(1)
            except AttributeError:
                print("Script Lyrics Failed, Try INT. or EXT. ")
                try:
                    main = re.search(r'[IE]{1}[NX]{1}T. (.*?)More on Genius', text, re.DOTALL).group(1)
                except AttributeError:
                    print("INT. or EXT. Failed, Try [Opening Credits] ")
                    try:
                        main = re.search(r'\[Opening Credits\](.*?)More on Genius', text, re.DOTALL).group(1)
                    except AttributeError:
                        continue
        main = main.strip()
        list = main.split("\n\n")
        my_df = pd.DataFrame({'lines':list})
        my_df['speaker'] = my_df['lines'].str.extract("(^.*:)")
        my_df['lines'] = my_df['lines'].str.replace("(^.*:)", '', regex=True)
        my_df['speaker'] = my_df['speaker'].replace(np.nan, 'SCENE:')
        my_df['speaker'] = my_df['speaker'].str.replace("(:)", '', regex=True)
        my_df['season'] = season_num
        my_df['episode'] = episode_num
        appending_frame = appending_frame.append(my_df, ignore_index=True)
appending_frame.to_pickle('RawEpsiode.pkl')


