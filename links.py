import json
import requests
from bs4 import BeautifulSoup, element
import pandas as pd

URL_FORMAT = 'https://pawpatrol.fandom.com/wiki/Category:Season_{season_int}_Episodes'
BASE_URL = 'https://pawpatrol.fandom.com'
LINK_FP_FORMAT = 'episode_urls/season_{season_num}_urls.txt'

NUM_SEASONS = 6

def get_links_for_season(season: int) -> list[str]:
    url = URL_FORMAT.format(season_int = season)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    divs = soup.find_all("div", class_="category-page__members")
    hrefs = []
    for div in divs:
        links = div.findAll('a')
        for a in links:
            try:
                href = a['href']
                hrefs.append(href)
            except BaseException as e:
                pass
    links=[]
    for href in hrefs:
        links.append(f'{BASE_URL}{href}')
    return set(links)

def main():
    for i in range(1, NUM_SEASONS + 1):
        season_links = get_links_for_season(i)
        fp = LINK_FP_FORMAT.format(season_num = i)
        with open(fp, 'w') as f:
            f.writelines('\n'.join(season_links))

if __name__ == '__main__':
    main()
