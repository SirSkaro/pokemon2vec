import time
from typing import List

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle

from .vgc_team import TeamFactory


class VictoryRoadVgcTeamFactory(TeamFactory):
    _TOURNAMENT_LISTING_PAGES = {
        '2024-season': 'https://victoryroadvgc.com/2024-season-calendar/'
    }

    _SAMPLE_TEAM_PAGES = {
        'sv-reg-a': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-a/',
        'sv-reg-b': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-b/',
        'sv-reg-c': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-c/',
        'sv-reg-d': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-d/',
        'sv-reg-e': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-e/',
        'sv-reg-f': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-f/',
        'sv-reg-g': 'https://victoryroadvgc.com/sv-rental-teams/',
        'sun-2019': 'https://victoryroadvgc.com/resources/sample-teams-for-vgc-2019-sun-series/',
        #'usum-2019': 'https://victoryroadvgc.com/resources/sample-teams-vgc19-ultra/',  # doesn't work
        'bdsp': 'https://victoryroadvgc.com/pokemon-bdsp-sample-vgc-teams/',
        'swsh-2022': 'https://victoryroadvgc.com/pokemon-sword-shield-rental-vgc-teams/',
        'swsh-2021': 'https://victoryroadvgc.com/pokemon-sword-shield-rental-vgc-teams-2021/',
        'swsh-2020': 'https://victoryroadvgc.com/pokemon-sword-shield-rental-vgc-teams-2020/'
    }

    def get_teams(self) -> List[List[str]]:
        return self._get_rental_teams()

    def _get_rental_teams(self) -> List[List[str]]:
        teams = []
        for page_name, url in self._SAMPLE_TEAM_PAGES.items():
            teams_on_page = self._get_rental_teams_on_page(page_name, url)
            for team in teams_on_page:
                teams.append(team)

        return teams

    def _get_rental_teams_on_page(self, page_name, url) -> List[List[str]]:
        filepath = f'data/victory_road/rental_teams/{page_name}.dat'
        try:
            team = pickle.load(open(filepath, 'rb'))
            return team
        except OSError as e:
            print(f'Cache miss for team {url}')
            team = self._fetch_teams_from_web(url)
            with open(filepath, 'wb') as f:
                pickle.dump(team, f)
            return team

    def _fetch_teams_from_web(self, url) -> List[List[str]]:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        print(f'Fetched rental_teams on page {url}. Sleeping to avoid rate limiting...')
        time.sleep(3.5)

        soup = BeautifulSoup(html, 'html.parser')
        all_teams_on_page = soup.find_all('div', {'class': 'table-team-wrapper'})
        return [self._extract_individual_team(team) for team in all_teams_on_page]

    def _extract_individual_team(self, team_div) -> List[str]:
        return [member['title'] for member in team_div.find_all('img')]
