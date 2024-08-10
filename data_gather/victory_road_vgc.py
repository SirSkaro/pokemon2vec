import time
from typing import List

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle

from .vgc_team import TeamFactory


class VictoryRoadVgcTeamFactory(TeamFactory):
    _EVENT_PAGES = {
        '2024-laic': 'https://victoryroadvgc.com/2024-laic/',
        '2024-euic': 'https://victoryroadvgc.com/2024-euic/',
        '2024-naic': 'https://victoryroadvgc.com/2024-naic/',
        '2024-korea': 'https://victoryroadvgc.com/2024-korea/',
        '2024-thailand': 'https://victoryroadvgc.com/2024-thailand/',
        '2024-singapore': 'https://victoryroadvgc.com/2024-singapore/',
        '2024-philippines': 'https://victoryroadvgc.com/2024-philippines/',
        '2024-japan': 'https://victoryroadvgc.com/2024-japan/',
        '2024-hong-kong': 'https://victoryroadvgc.com/2024-hong-kong/',
        '2024-taiwan': 'https://victoryroadvgc.com/2024-taiwan/',
        '2024-malaysia': 'https://victoryroadvgc.com/2024-malaysia/',
        '2024-pittsburgh': 'https://victoryroadvgc.com/2024-pittsburgh/',
        '2024-peoria': 'https://victoryroadvgc.com/2024-peoria/',
        '2024-sacramento': 'https://victoryroadvgc.com/2024-sacramento/',
        '2024-toronto': 'https://victoryroadvgc.com/2024-toronto/',
        '2024-san-antonio': 'https://victoryroadvgc.com/2024-san-antonio/',
        '2024-portland': 'https://victoryroadvgc.com/2024-portland/',
        '2024-charlotte': 'https://victoryroadvgc.com/2024-charlotte/',
        '2024-knoxville': 'https://victoryroadvgc.com/2024-knoxville/',
        '2024-vancouver': 'https://victoryroadvgc.com/2024-vancouver/',
        '2024-orlando': 'https://victoryroadvgc.com/2024-orlando/',
        '2024-indianapolis': 'https://victoryroadvgc.com/2024-indianapolis/',
        '2024-carolina': 'https://victoryroadvgc.com/2024-carolina/',
        '2024-los-angeles': 'https://victoryroadvgc.com/2024-los-angeles/',
        '2024-barcelona': 'https://victoryroadvgc.com/2024-barcelona/',
        '2024-lille': 'https://victoryroadvgc.com/2024-lille/',
        '2024-gdansk': 'https://victoryroadvgc.com/2024-gdansk/',
        '2024-stuttgart': 'https://victoryroadvgc.com/2024-stuttgart/',
        '2024-liverpool': 'https://victoryroadvgc.com/2024-liverpool/',
        '2024-dortmund': 'https://victoryroadvgc.com/2024-dortmund',
        '2024-utrecht': 'https://victoryroadvgc.com/2024-utrecht/',
        '2024-stockholm': 'https://victoryroadvgc.com/2024-stockholm/',
        '2024-bologna': 'https://victoryroadvgc.com/2024-bologna/',
        '2024-curitiba': 'https://victoryroadvgc.com/2024-curitiba/',
        '2024-goiania': 'https://victoryroadvgc.com/2024-goiania/',
        '2024-sao-paulo': 'https://victoryroadvgc.com/2024-sao-paulo/',
        '2024-buenos-aires': 'https://victoryroadvgc.com/2024-buenos-aires/',
        '2024-bogota': 'https://victoryroadvgc.com/2024-bogota/',
        '2024-santiago': 'https://victoryroadvgc.com/2024-santiago/',
        '2024-lima': 'https://victoryroadvgc.com/2024-lima/',
        '2024-mexico-city': 'https://victoryroadvgc.com/2024-mexico-city/',
        '2024-brisbane': 'https://victoryroadvgc.com/2024-brisbane/',
        '2024-melbourne': 'https://victoryroadvgc.com/2024-melbourne/',
        '2024-perth': 'https://victoryroadvgc.com/2024-perth/',
        'vr-september-2023': 'https://victoryroadvgc.com/vr-september-2023/',
        'vr-winter-challenge-2024': 'https://victoryroadvgc.com/vr-winter-challenge/',
        'vr-spring-challenge-2024': 'https://victoryroadvgc.com/vr-spring-challenge/',
        'vr-road-honolulu-2024': 'https://victoryroadvgc.com/vr-road-honolulu/',
        'vr-road-honolulu-2-2024': 'https://victoryroadvgc.com/vr-road-honolulu-2/',
        'winter-festa-2023': 'https://victoryroadvgc.com/winter-festa/',
        'ryuo-sen-2024': 'https://victoryroadvgc.com/2024-ryuo-sen/'
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
