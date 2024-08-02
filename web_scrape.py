from typing import List

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re


def fetch_team_ids(page_size) -> List[int]:
    req = Request(f'https://limitlessvgc.com/teams/?show={page_size}', headers={'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req).read()

    soup = BeautifulSoup(html_page, 'html.parser')
    team_urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/teams/')]
    return [int(url.split('/')[2]) for url in team_urls]

