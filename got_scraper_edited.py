
#%%
from lxml import html
import requests
import re
import pandas as pd
import BeautifulSoup


#%%
def process(season, episode, stripped):
    filtered = [s for s in stripped if not s.startswith("/") and s != "More on Genius"]
    labeled = []
    for f in filtered:
        m = re.search('([A-Z ]+):(.*)', f)
        if m:
            labeled.append([m.group(1),m.group(2)])
        elif f.startswith("["):
            labeled.append(["SCENE", f])
        else:
            labeled.append([f])
    merged = []
    chunks = []
    cur = "DEFAULT"
    for l in labeled:
        if len(l) >1:
            merged.append([cur,chunks])
            chunks = []
            cur = l[0]
            chunks.append(l[1])
        else:
            chunks.append(l[0])

    return [[season, episode, m[0], " ".join(m[1]).strip()] for m in merged]



#%%
# these were in bad shape:
#  "https://genius.com/albums/Game-of-thrones/Season-7-scripts"


seasons = [
    # "https://genius.com/albums/Game-of-thrones/Season-1-scripts",
    # "https://genius.com/albums/Game-of-thrones/Season-2-scripts",
    # "https://genius.com/albums/Game-of-thrones/Season-3-scripts",
    # "https://genius.com/albums/Game-of-thrones/Season-4-scripts",
    # "https://genius.com/albums/Game-of-thrones/Season-5-scripts",
    # "https://genius.com/albums/Game-of-thrones/Season-6-scripts",
    "https://genius.com/albums/Game-of-thrones/Season-7-scripts"
]

episodes = [];
for sidx, url in enumerate(seasons, start = 1):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    ep_urls = tree.xpath("//div[contains(@class, 'chart_row')]/a/@href") 
    print(ep_urls)
    for eidx, ep in enumerate(ep_urls, start = 1):
        print(sidx, eidx, ep)
        page = requests.get(ep)
#%%
print(page.content)
print(page.text)
#%%


#%%
    ep_urls = tree.xpath("//div[contains(@class, 'chart_row')]/a/@href")    
    for eidx, ep in enumerate(ep_urls):
        if "needs-editing" in ep:
            print("skipping: ", ep)
            continue
        print(sidx, eidx, ep)
        page = requests.get(ep)
        tree = html.fromstring(page.content)
        raw = tree.xpath("//div[contains(@class, 'lyrics')]/descendant::*/text()")
        stripped = [r.strip() for r in raw if r.strip() != '']
        processed = process(sidx, eidx, stripped)
        episodes = episodes + processed
    


#%%
dat = pd.DataFrame(episodes)
dat.columns = ["season_idx", "episode_idx", "character", "utterance"]
dat.to_csv("got.csv")


#%%
pd.options.display.max_colwidth = 1000
dat


