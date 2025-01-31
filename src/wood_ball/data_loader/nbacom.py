import duckdb
import polars as pl
from typing import List, Dict 
from nba_api.stats.endpoints import shotchartdetail, commonplayerinfo, teaminfocommon, boxscoreadvancedv2, leaguegamelog, boxscoretraditionalv2
from nba_api.stats.static import players, teams
import wood_ball.data_loader.data_load_strings as data_load_strings
from rich.progress import track
from rich import print
import time

class NBAComLoader:
    """
    A class that will load nba to users Motherduck account or to a local duckdb of the users choosing
    """
    def __init__(self, motherduck_token: str = "", local_db_path: str = ':memory:', duckdb_connection=None):
        """
        Initialize the motherduck token and local duckdb path

        Args:
            motherduck_token (str): motherduck token to be used to load data to motherduck
            local_db_path (str, optional): the local duckdb path to load the data to. Defaults to ':memory:' which means all data will be lost when python process is exited.
        """
        
        # self.connection_string
        self.loop_rest_time = .15

        print("[dark_orange]<-------NBAComLoader------------------------------->[/dark_orange]")
        # may need to modify this to try except
        if duckdb_connection is not None:
            self.con = duckdb_connection
        elif motherduck_token != "":
            self.duck_connection_string = f'md:nba_data?motherduck_token={motherduck_token}'
            self.db_display_name = 'md:nba_data'
            self.con = duckdb.connect(f'{self.duck_connection_string}')
        elif local_db_path == ':memory:':
            self.duck_connection_string = local_db_path
            self.db_display_name = local_db_path
            print('Using in-memory duckdb database')
            self.con = duckdb.connect(f'{self.duck_connection_string}')
        elif local_db_path != ':memory:':
            self.duck_connection_string = local_db_path
            self.db_display_name = local_db_path
            print(f'Using {local_db_path} as duckdb db path')
            self.con = duckdb.connect(f'{self.duck_connection_string}')

    def load_data_to_duckdb(self, nba_data: List[Dict[any, any]], query_string: str, schema: str = 'main', table: str = 'None'):
        """Load any of the standard python data structures of python data
            to selected duckdb database

        Args:
            nba_data (List[Dict[any, any]]): nba_stats objects responses (nba_api)
            query_string (str): query string starting and ending with select provided in query module
            database (str, optional): Explicitly describe database. Defaults to 'nba_data'.
            table (str, optional): Explicitly describe table. Defaults to 'None'.

        Raises:
            Exception: Verifies that a table name was provided to the method.
        """        
        if table == 'None':
            raise Exception("No Table Name provided.")
        
        source_df = pl.DataFrame(nba_data)

        self.con.execute(f"""
        INSERT OR REPLACE INTO {schema}.{table} {query_string}
        from source_df
            """)
    
    def create_duckdb_tables(self, query_string: str, schema: str = 'main', table: str = 'None'):
        """Generic function to check if table exists in target duckdb location, whether that is in Motherduck or in a local
            duckdb

        Args:
            query_string (str): DuckDB query string specifying the table definition along with the constraints
            schema (str, optional): Target schema name. Defaults to 'main'.
            table (str, optional): Target table name. Defaults to 'None'.
        """        
        self.con.execute(f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table}
                         ({query_string})
                 """)
    
    def load_box_scores(self, date_from: str, date_to: str, season_type_all_star: str = "Regular Season",):
        """Method to load box scores, have to load game logs to load box scored

        Args:
            date_from (str): Example value '2025-08-01'. I need to decide if these are inclusive.  
            date_to (str): Example value '2025-10-01'.
        """

        game_log = leaguegamelog.LeagueGameLog(
            season_type_all_star=season_type_all_star,
            date_from_nullable=date_from,
            date_to_nullable=date_to,            
        ).get_normalized_dict()["LeagueGameLog"]
        # load game log
        self.create_duckdb_tables(query_string=data_load_strings.create_nba_game_log_table, table='nba_game_log')
        self.load_data_to_duckdb(
            nba_data=game_log, 
            query_string= 'select *',
            table='nba_game_log'
            )
        
        game_log_df = self.con.execute(
            """
        select * from main.nba_game_log
        where CAST(GAME_DATE as DATE) between CAST(? as DATE) and CAST(? as DATE)
        """,
            [date_from, date_to], # modify before running for now
        ).pl()

        game_id_list = game_log_df["GAME_ID"].unique().to_list()
        print('Game ID list pulled, using to get box scores now...')

        # using nba_api to load here rather than creating an unecessary module
        box_score_advanced_obj_list = [boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id) for game_id in track(game_id_list, description="Advanced Box Score stats...") if time.sleep(self.loop_rest_time) is None]
        box_adv_team = [player_stats for box_score in box_score_advanced_obj_list for player_stats in box_score.get_normalized_dict()["TeamStats"]]
        box_adv_players = [player_stats for box_score in box_score_advanced_obj_list for player_stats in box_score.get_normalized_dict()["PlayerStats"]]

        trad_box_score_obj_list = [boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id) for game_id in track(game_id_list, description="Traditional Box Score Stats...") if time.sleep(self.loop_rest_time) is None]
        box_trad_players = [player_stats for box_score in trad_box_score_obj_list for player_stats in box_score.get_normalized_dict()["PlayerStats"]]
        box_trad_team = [player_stats for box_score in trad_box_score_obj_list for player_stats in box_score.get_normalized_dict()["TeamStats"]]

        # print('Creating box_adv_player table if not already exists.')
        # box adv player
        table_name = 'box_adv_player'
        self.create_duckdb_tables(query_string=data_load_strings.create_box_adv_player_table, table=table_name)
        # print('Loading data to box_adv_player')
        self.load_data_to_duckdb(
            nba_data=box_adv_players, 
            query_string= data_load_strings.box_adv_player_query_string,
            table=table_name
            )
        
        # print('Creating box_adv_team table if not already exists.')
        # box adv team
        table_name = 'box_adv_team'
        self.create_duckdb_tables(query_string=data_load_strings.create_box_adv_team_table, table=table_name)
        # print('Loading data to box_adv_team')
        self.load_data_to_duckdb(
            nba_data=box_adv_team, 
            query_string= data_load_strings.box_adv_team_query_string,
            table=table_name
            )
        
        # print('Creating box_trad_player table if not already exists.')
        # box trad player
        table_name = 'box_trad_player'
        self.create_duckdb_tables(query_string=data_load_strings.create_box_trad_player_table, table=table_name)
        # print('Loading data to box_trad_player')
        self.load_data_to_duckdb(
            nba_data=box_trad_players, 
            query_string= data_load_strings.box_trad_player_query_string,
            table=table_name
            )
        
        # print('Creating box_trad_team table if not already exists.')
        # box trad teams
        table_name = 'box_trad_team'
        self.create_duckdb_tables(query_string=data_load_strings.create_box_trad_team_table, table=table_name)
        # print('Loading data to box_trad_team')
        self.load_data_to_duckdb(
            nba_data=box_trad_team, 
            query_string= data_load_strings.box_trad_team_query_string,
            table=table_name
            )
        
        print(f"[bold magenta]Box Scores (advanced player/team, traditional player/team)[/bold magenta] have been loaded to [bold dark_orange]{self.db_display_name}[/bold dark_orange]")
        print("[dark_orange]<-------NBAComLoader------------------------------->[/dark_orange]")
