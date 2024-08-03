from typing import List

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle

from .vgc_team import TeamFactory

class LimitlessVgcTeamFactory(TeamFactory):

    def get_teams(self) -> List[List[str]]:
        pass

    def _get_team_ids(self) -> List[int]:
        try:
            return pickle.load(open('data/limitless/team_ids.dat', 'rb'))
        except(OSError) as e:
            ids = self._fetch_team_ids(500)
            self._store_team_ids(ids)
            return ids


    def _fetch_team_ids(self, page_size) -> List[int]:
        req = Request(f'https://limitlessvgc.com/teams/?show={page_size}', headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()

        soup = BeautifulSoup(html_page, 'html.parser')
        team_urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/teams/')]
        return [int(url.split('/')[2]) for url in team_urls]


    def _store_team_ids(self, team_ids):
        with open('data/limitless/team_ids.dat', 'wb') as f:
            pickle.dump(team_ids, f)

