import requests
from lib.creds import odds_api_key
import pandas as pd
from rich import print
import duckdb
from datetime import datetime, timedelta


class Odds:
    def __init__(self):
        self.API_KEY = odds_api_key

    def get_sports(self):
        sports_response = requests.get(
            "https://api.the-odds-api.com/v4/sports", params={"api_key": self.API_KEY}
        )
        return pd.DataFrame(sports_response.json())

    def get_usage(self):
        odds_response = requests.get(
            "https://api.the-odds-api.com/v4/sports", params={"api_key": self.API_KEY}
        )
        print("Remaining requests:", odds_response.headers["x-requests-remaining"])
        print("Used requests:", odds_response.headers["x-requests-used"])

    def get_nba_champ_odds(self):
        sport = "basketball_nba_championship_winner"
        odds_response = requests.get(
            f"https://api.the-odds-api.com/v4/sports/{sport}/odds",
            params={
                "api_key": self.API_KEY,
                "regions": "us",
                "markets": "outrights",
                "oddsFormat": "decimal",
                "dateFormat": "iso",
            },
        )

        if odds_response.status_code != 200:
            print(
                f"Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}"
            )

        else:
            odds_json = odds_response.json()
            print("Number of events:", len(odds_json))

            # Check the usage quota
            print("Remaining requests", odds_response.headers["x-requests-remaining"])
            print("Used requests", odds_response.headers["x-requests-used"])

        odds_meta = [
            ["id"],
            ["has_outrights"],
            ["sport_key"],
            ["sport_title"],
            ["commence_time"],
            ["home_team"],
            ["away_team"],
            ["bookmakers", "key"],
            ["bookmakers", "title"],
            ["bookmakers", "last_update"],
            ["bookmakers", "markets", "key"],
            ["bookmakers", "markets", "last_update"],
        ]

        df = pd.json_normalize(
            odds_json,
            record_path=["bookmakers", "markets", "outcomes"],
            meta=odds_meta,
            sep="_",
        )
        return df

    def get_ncaa_champ_odds(self):
        sport = "basketball_ncaa_championship_winner"
        odds_response = requests.get(
            f"https://api.the-odds-api.com/v4/sports/{sport}/odds",
            params={
                "api_key": self.API_KEY,
                "regions": "us",
                "markets": "outrights",
                "oddsFormat": "decimal",
                "dateFormat": "iso",
            },
        )

        if odds_response.status_code != 200:
            print(
                f"Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}"
            )

        else:
            odds_json = odds_response.json()
            print("Number of events:", len(odds_json))

            # Check the usage quota
            print("Remaining requests", odds_response.headers["x-requests-remaining"])
            print("Used requests", odds_response.headers["x-requests-used"])

        odds_meta = [
            ["id"],
            ["has_outrights"],
            ["sport_key"],
            ["sport_title"],
            ["commence_time"],
            ["home_team"],
            ["away_team"],
            ["bookmakers", "key"],
            ["bookmakers", "title"],
            ["bookmakers", "last_update"],
            ["bookmakers", "markets", "key"],
            ["bookmakers", "markets", "last_update"],
        ]

        df = pd.json_normalize(
            odds_json,
            record_path=["bookmakers", "markets", "outcomes"],
            meta=odds_meta,
            sep="_",
        )
        return df

    def get_commencement_times(self):
        # Get current ISO time
        current_iso_time = (
            datetime.now().replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
        )

        print("Current ISO Time: ", current_iso_time)

        # Calculate 20 hours from now
        future_time = datetime.now() + timedelta(hours=20)
        future_iso_time = future_time.replace(microsecond=0).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        print("20 Hours From Now (ISO Time): ", future_iso_time)

        return current_iso_time, future_iso_time

    def get_next_24hr_nba_game_odds(self):
        # name sport key for nba api
        sport = "basketball_nba"

        # determine times to pass as reference in parameters
        current_iso_time, future_iso_time = self.get_commencement_times()
        odds_response = requests.get(
            f"https://api.the-odds-api.com/v4/sports/{sport}/odds",
            params={
                "api_key": self.API_KEY,
                "regions": "us",
                "markets": "h2h",
                "oddsFormat": "american",
                "dateFormat": "iso",
                "bookmakers": ["betmgm", "fanduel", "draftkings"],
                "commenceTimeFrom": current_iso_time,
                "commenceTimeTo": future_iso_time,
            },
        )

        # catch errors and print requests
        if odds_response.status_code != 200:
            print(
                f"Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}"
            )

        else:
            odds_json = odds_response.json()
            print("Number of events:", len(odds_json))
            print(odds_json)

            # Check the usage quota
            print("Remaining requests", odds_response.headers["x-requests-remaining"])
            print("Used requests", odds_response.headers["x-requests-used"])

        # declare schema
        odds_meta = [
            ["id"],
            ["sport_key"],
            ["sport_title"],
            ["commence_time"],
            ["home_team"],
            ["away_team"],
            ["bookmakers", "key"],
            ["bookmakers", "title"],
            ["bookmakers", "last_update"],
            ["bookmakers", "markets", "key"],
            ["bookmakers", "markets", "last_update"],
        ]

        # set path where data exists in list
        df = pd.json_normalize(
            odds_json,
            record_path=["bookmakers", "markets", "outcomes"],
            meta=odds_meta,
            sep="_",
        )

        return df

    def append_to_table(df, table_name, db_path="X:\\nba_data\\odds_data\\odds.db"):
        """
        Appends data from a DataFrame to the ncaa_champ_odds table in the DuckDB database.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the data to append.
        db_path (str): The path to the DuckDB database file.
        """

        df["load_date"] = pd.to_datetime("today").strftime("%Y-%m-%d")
        # Connect to the DuckDB database
        conn = duckdb.connect(db_path)

        # Check if the ncaa_champ_odds table exists
        table_exists = conn.execute(
            f"SELECT * FROM information_schema.tables WHERE table_name = '{table_name}'"
        ).fetchone()

        if table_exists:
            # Append the data to the ncaa_champ_odds table
            conn.execute(f"INSERT INTO '{table_name}' SELECT * FROM df")
            print("Data appended successfully.")
        else:
            conn.execute(f"CREATE TABLE '{table_name}' AS SELECT * FROM df")
            print(f"Table {table_name} does not exist. Created table from DF")

        # Close the connection
        conn.close()
