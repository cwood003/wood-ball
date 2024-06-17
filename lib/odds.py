import requests
from lib.creds import odds_api_key
import pandas as pd
from rich import print

class Odds:
    def __init__(self):
        self.API_KEY = odds_api_key
    
    def get_sports(self):
        sports_response = requests.get(
            'https://api.the-odds-api.com/v4/sports', 
            params={
                'api_key': self.API_KEY
            }
        )
        return pd.DataFrame(sports_response.json())

    def get_usage(self):
        odds_response = requests.get(
            'https://api.the-odds-api.com/v4/sports', 
            params={
                'api_key': self.API_KEY
            }
        )
        print('Remaining requests:', odds_response.headers['x-requests-remaining'])
        print('Used requests:', odds_response.headers['x-requests-used'])

    
    def get_nba_champ_odds(self):

        sport = 'basketball_nba_championship_winner'
        odds_response = requests.get(
            f'https://api.the-odds-api.com/v4/sports/{sport}/odds',
            params={
                'api_key': self.API_KEY,
                'regions': 'us',
                'markets': 'outrights',
                'oddsFormat': 'decimal',
                'dateFormat': 'iso',
            }
        )

        if odds_response.status_code != 200:
            print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

        else:
            odds_json = odds_response.json()
            print('Number of events:', len(odds_json))

        odds_meta = [
            ['id'],
            ['has_outrights'],
            ['sport_key'],
            ['sport_title'],
            ['commence_time'],
            ['home_team'],
            ['away_team'],
            ['bookmakers', 'key'],
            ['bookmakers', 'title'],
            ['bookmakers', 'last_update'],
            ['bookmakers', 'markets', 'key'],
            ['bookmakers', 'markets', 'last_update']
        ]

        df = pd.json_normalize(odds_json, record_path=['bookmakers', 'markets', 'outcomes'], 
                    meta=odds_meta, sep='_'
                    )
        return df
