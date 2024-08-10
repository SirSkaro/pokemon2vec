from typing import List

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle

from .vgc_team import TeamFactory


class WorldCupVgcTeamFactory(TeamFactory):
    _HUB_PAGES = {
        '2021': 'https://2021.worldcupvgc.com/teams'
    }

    def get_teams(self) -> List[List[str]]:
        pass

    def _get_player_team_links(self, hub_page_url):
        req = Request(f'{hub_page_url}/teams', headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()

        soup = BeautifulSoup(html, 'html.parser')
        team_urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/teams/')]
        return set([int(url.split('/')[2]) for url in team_urls])