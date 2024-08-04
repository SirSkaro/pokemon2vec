import time
from typing import List

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle

from .vgc_team import TeamFactory


class VictoryRoadVgcTeamFactory(TeamFactory):
    # TODO make this a map
    _SAMPLE_TEAM_PAGES = [
        'https://victoryroadvgc.com/sv-rental-teams-reg-set-a/',
        'https://victoryroadvgc.com/sv-rental-teams-reg-set-b/',
        'https://victoryroadvgc.com/sv-rental-teams-reg-set-c/',
        'https://victoryroadvgc.com/sv-rental-teams-reg-set-d/',
        'https://victoryroadvgc.com/sv-rental-teams-reg-set-e/',
        'https://victoryroadvgc.com/sv-rental-teams-reg-set-f/',
        'https://victoryroadvgc.com/sv-rental-teams/',  # regulation G
        'https://victoryroadvgc.com/resources/sample-teams-for-vgc-2019-sun-series/',
        # 'https://victoryroadvgc.com/resources/sample-teams-vgc19-ultra/',  # doesn't work
        'https://victoryroadvgc.com/pokemon-bdsp-sample-vgc-teams/',
        'https://victoryroadvgc.com/pokemon-sword-shield-rental-vgc-teams/',
        'https://victoryroadvgc.com/pokemon-sword-shield-rental-vgc-teams-2021/',
        'https://victoryroadvgc.com/pokemon-sword-shield-rental-vgc-teams-2020/'
    ]

    def get_teams(self) -> List[List[str]]:
        pass

    def _get_teams_on_page(self, url) -> List[str]:
        # TODO
        pass

    def _fetch_teams_from_web(self, page) -> List[List[str]]:
        req = Request(page, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        print(f'Fetched teams on page {page}. Sleeping to avoid rate limiting...')
        time.sleep(3.5)

        soup = BeautifulSoup(html, 'html.parser')
        all_teams_on_page = soup.find_all('div', {'class': 'table-team-wrapper'})
        return [self._extract_individual_team(team) for team in all_teams_on_page]

    def _extract_individual_team(self, team_div) -> List[str]:
        return [member['title'] for member in team_div]