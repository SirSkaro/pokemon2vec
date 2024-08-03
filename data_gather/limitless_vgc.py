from typing import List, Set

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle

from .vgc_team import TeamFactory


class LimitlessVgcTeamFactory(TeamFactory):

    def get_teams(self) -> List[Set[str]]:
        pass

    def _get_team_ids(self) -> Set[int]:
        filepath = 'data/limitless/team_ids.dat'
        try:
            return pickle.load(open(filepath, 'rb'))
        except OSError as e:
            ids = self._fetch_team_ids(500)
            with open(filepath, 'wb') as f:
                pickle.dump(ids, f)
            return ids

    def _fetch_team_ids(self, page_size) -> Set[int]:
        req = Request(f'https://limitlessvgc.com/teams/?show={page_size}', headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()

        soup = BeautifulSoup(html_page, 'html.parser')
        team_urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/teams/')]
        return set([int(url.split('/')[2]) for url in team_urls])

