import time
from typing import List, Set

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle

from .vgc_team import TeamFactory


class LimitlessVgcTeamFactory(TeamFactory):
    _WEB_BASE_URI = 'https://limitlessvgc.com'

    def get_teams(self) -> List[List[str]]:
        ids = self._get_team_ids()
        teams = []
        for id in ids:
            team = self._get_team_by_id(id)
            teams.append(team)
        return teams

    def _get_team_ids(self) -> Set[int]:
        filepath = 'data/limitless/team_ids.dat'
        try:
            return pickle.load(open(filepath, 'rb'))
        except OSError as e:
            ids = self._fetch_team_ids_from_web(500)
            with open(filepath, 'wb') as f:
                pickle.dump(ids, f)
            return ids

    def _fetch_team_ids_from_web(self, page_size) -> Set[int]:
        req = Request(f'{self._WEB_BASE_URI}/teams/?show={page_size}', headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()

        soup = BeautifulSoup(html, 'html.parser')
        team_urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/teams/')]
        return set([int(url.split('/')[2]) for url in team_urls])

    def _get_team_by_id(self, id) -> List[str]:
        filepath = f'data/limitless/teams/{id}.dat'
        try:
            team = pickle.load(open(filepath, 'rb'))
            return team
        except OSError as e:
            print(f'Cache miss for team {id}')
            team = self._fetch_team_from_web(id)
            with open(filepath, 'wb') as f:
                pickle.dump(team, f)
            return team

    def _fetch_team_from_web(self, id) -> List[str]:
        req = Request(f'{self._WEB_BASE_URI}/teams/{id}', headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        print(f'Fetched team {id}. Sleeping to avoid rate limiting...')
        time.sleep(3.5)

        soup = BeautifulSoup(html, 'html.parser')
        return [a.get_text() for a in soup.find_all('a', {'class': 'pokemon-link'})]


