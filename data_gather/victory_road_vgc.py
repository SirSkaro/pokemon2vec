import time
from typing import List, Dict

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle

from .vgc_team import TeamFactory


class VictoryRoadVgcTeamFactory(TeamFactory):
    _EVENT_PAGES = {
        'events/2024-laic': 'https://victoryroadvgc.com/2024-laic/',
        'events/2024-euic': 'https://victoryroadvgc.com/2024-euic/',
        'events/2024-naic': 'https://victoryroadvgc.com/2024-naic/',
        'events/2024-korea': 'https://victoryroadvgc.com/2024-korea/',
        'events/2024-thailand': 'https://victoryroadvgc.com/2024-thailand/',
        'events/2024-singapore': 'https://victoryroadvgc.com/2024-singapore/',
        'events/2024-philippines': 'https://victoryroadvgc.com/2024-philippines/',
        'events/2024-japan': 'https://victoryroadvgc.com/2024-japan/',
        'events/2024-hong-kong': 'https://victoryroadvgc.com/2024-hong-kong/',
        'events/2024-taiwan': 'https://victoryroadvgc.com/2024-taiwan/',
        'events/2024-malaysia': 'https://victoryroadvgc.com/2024-malaysia/',
        'events/2024-pittsburgh': 'https://victoryroadvgc.com/2024-pittsburgh/',
        'events/2024-peoria': 'https://victoryroadvgc.com/2024-peoria/',
        'events/2024-sacramento': 'https://victoryroadvgc.com/2024-sacramento/',
        'events/2024-toronto': 'https://victoryroadvgc.com/2024-toronto/',
        'events/2024-san-antonio': 'https://victoryroadvgc.com/2024-san-antonio/',
        'events/2024-portland': 'https://victoryroadvgc.com/2024-portland/',
        'events/2024-charlotte': 'https://victoryroadvgc.com/2024-charlotte/',
        'events/2024-knoxville': 'https://victoryroadvgc.com/2024-knoxville/',
        'events/2024-vancouver': 'https://victoryroadvgc.com/2024-vancouver/',
        'events/2024-orlando': 'https://victoryroadvgc.com/2024-orlando/',
        'events/2024-indianapolis': 'https://victoryroadvgc.com/2024-indianapolis/',
        'events/2024-carolina': 'https://victoryroadvgc.com/2024-carolina/',
        'events/2024-los-angeles': 'https://victoryroadvgc.com/2024-los-angeles/',
        'events/2024-barcelona': 'https://victoryroadvgc.com/2024-barcelona/',
        'events/2024-lille': 'https://victoryroadvgc.com/2024-lille/',
        'events/2024-gdansk': 'https://victoryroadvgc.com/2024-gdansk/',
        'events/2024-stuttgart': 'https://victoryroadvgc.com/2024-stuttgart/',
        'events/2024-liverpool': 'https://victoryroadvgc.com/2024-liverpool/',
        'events/2024-dortmund': 'https://victoryroadvgc.com/2024-dortmund',
        'events/2024-utrecht': 'https://victoryroadvgc.com/2024-utrecht/',
        'events/2024-stockholm': 'https://victoryroadvgc.com/2024-stockholm/',
        'events/2024-bologna': 'https://victoryroadvgc.com/2024-bologna/',
        'events/2024-curitiba': 'https://victoryroadvgc.com/2024-curitiba/',
        'events/2024-goiania': 'https://victoryroadvgc.com/2024-goiania/',
        'events/2024-sao-paulo': 'https://victoryroadvgc.com/2024-sao-paulo/',
        'events/2024-buenos-aires': 'https://victoryroadvgc.com/2024-buenos-aires/',
        'events/2024-bogota': 'https://victoryroadvgc.com/2024-bogota/',
        'events/2024-santiago': 'https://victoryroadvgc.com/2024-santiago/',
        'events/2024-lima': 'https://victoryroadvgc.com/2024-lima/',
        'events/2024-mexico-city': 'https://victoryroadvgc.com/2024-mexico-city/',
        'events/2024-brisbane': 'https://victoryroadvgc.com/2024-brisbane/',
        'events/2024-melbourne': 'https://victoryroadvgc.com/2024-melbourne/',
        'events/2024-perth': 'https://victoryroadvgc.com/2024-perth/',
        'events/2023-vr-september': 'https://victoryroadvgc.com/vr-september-2023/',
        'events/2024-vr-winter-challenge': 'https://victoryroadvgc.com/vr-winter-challenge/',
        'events/2024-vr-spring-challenge': 'https://victoryroadvgc.com/vr-spring-challenge/',
        'events/2024-vr-road-honolulu': 'https://victoryroadvgc.com/vr-road-honolulu/',
        'events/2024-vr-road-honolulu-2': 'https://victoryroadvgc.com/vr-road-honolulu-2/',
        'events/2023-winter-festa': 'https://victoryroadvgc.com/winter-festa/',
        'events/2024-ryuo-sen': 'https://victoryroadvgc.com/2024-ryuo-sen/'
    }

    _SAMPLE_TEAM_PAGES = {
        'rental_teams/sv-reg-a': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-a/',
        'rental_teams/sv-reg-b': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-b/',
        'rental_teams/sv-reg-c': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-c/',
        'rental_teams/sv-reg-d': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-d/',
        'rental_teams/sv-reg-e': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-e/',
        'rental_teams/sv-reg-f': 'https://victoryroadvgc.com/sv-rental-teams-reg-set-f/',
        'rental_teams/sv-reg-g': 'https://victoryroadvgc.com/sv-rental-teams/',
        'rental_teams/sun-2019': 'https://victoryroadvgc.com/resources/sample-teams-for-vgc-2019-sun-series/',
        #'usum-2019': 'https://victoryroadvgc.com/resources/sample-teams-vgc19-ultra/',  # doesn't work
        'rental_teams/bdsp': 'https://victoryroadvgc.com/pokemon-bdsp-sample-vgc-teams/',
        'rental_teams/swsh-2022': 'https://victoryroadvgc.com/pokemon-sword-shield-rental-vgc-teams/',
        'rental_teams/swsh-2021': 'https://victoryroadvgc.com/pokemon-sword-shield-rental-vgc-teams-2021/',
        'rental_teams/swsh-2020': 'https://victoryroadvgc.com/pokemon-sword-shield-rental-vgc-teams-2020/'
    }

    def get_teams(self) -> List[List[str]]:
        return self._get_teams_on_pages({**self._SAMPLE_TEAM_PAGES, **self._EVENT_PAGES})

    def _get_teams_on_pages(self, pages: Dict[str, str]) -> List[List[str]]:
        teams = []
        for page_name, url in pages.items():
            teams_on_page = self._get_teams_on_page(page_name, url)
            for team in teams_on_page:
                teams.append(team)

        return teams

    def _get_teams_on_page(self, page_name, url) -> List[List[str]]:
        filepath = f'data/victory_road/{page_name}.dat'
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
        print(f'Fetched teams on page {url}. Sleeping to avoid rate limiting...')
        time.sleep(3.5)

        soup = BeautifulSoup(html, 'html.parser')
        all_teams_on_page = soup.find_all('div', {'class': 'table-team-wrapper'})
        return [self._extract_individual_team(team) for team in all_teams_on_page]

    def _extract_individual_team(self, team_div) -> List[str]:
        return [member['title'] for member in team_div.find_all('img')]
