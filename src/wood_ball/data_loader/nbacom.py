from wood_ball.stats.nba_stats import NBA_Stats
import duckdb
import polars as pl
from typing import List, Dict 
import wood_ball.data_loader.data_load_strings as data_load_strings

class NBAComLoader:
    """
    A class that will load nba to users Motherduck account or to a local duckdb of the users choosing
    """
    def __init__(self, motherduck_token: str = "", local_db_path: str = 'my_duckdb.duckdb'):
        """
        Initialize the motherduck token and local duckdb path

        Args:
            motherduck_token (str): motherduck token to be used to load data to motherduck
            local_db_path (str, optional): the local duckdb path to load the data to. Defaults to 'my_duckdb.duckdb'.
        """
        
        self.motherduck_token = motherduck_token
        self.local_db_path = local_db_path
        self.nba_client = NBA_Stats()

        # may need to modify this to try except
        if motherduck_token != "":
            self.con = duckdb.connect(f'md:?motherduck_token={motherduck_token}')
        elif local_db_path == 'my_duckdb.duckdb':
            print('Using Current Directory to write duckdb db')
            self.con = duckdb.connect(f'{local_db_path}')
        elif local_db_path != 'my_duckdb.duckdb':
            print(f'Using {local_db_path} as duckdb db path')
            self.con = duckdb.connect(f'{local_db_path}')

    def load_data_to_duckdb(self, nba_data: List[Dict[any, any]], query_string: str, database: str = 'nba_data', table: str = 'None'):
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
        INSERT OR REPLACE INTO {database}.{table} {query_string}
        from source_df
            """)
    
    def create_duckdb_tables(self, query_string: str, database: str = 'nba_data', table: str = 'None'):
        self.con.execute(f"""
            CREATE TABLE IF NOT EXISTS {database}.{table}
                         ({query_string})
                 """)
    
    def load_box_scores(self, date_from: str, date_to: str):
        """Method to load box scores, have to load game logs to load box scored

        Args:
            date_from (str): Example value '01-08-2025'. I need to decide if these are inclusive.  
            date_to (str): Example value '01-10-2025'.
        """

        game_log = self.nba_client.get_game_log(date_from=date_from, date_to=date_to)
        # load game log
        self.create_duckdb_tables(query_string=data_load_strings.create_nba_game_log_table, table='nba_game_log')
        self.load_data_to_duckdb(
            nba_data=game_log, 
            query_string= 'select *',
            table='nba_game_log'
            )
        
        game_log_df = self.con.execute(
            """
        select * from nba_data.nba_game_log
        where GAME_DATE between CAST(? as DATE) and CAST(? as DATE)
        """,
            [date_from, date_to], # modify before running for now
        ).pl()

        game_id_list = game_log_df["GAME_ID"].unique().to_list()
        print('Game ID list pulled, using to get box scores now...')

        box_adv_players, box_adv_team = self.nba_client.get_box_scores(game_id_list, 'adv')
        print('Advanced box scores pulled into objects.')
        box_trad_players, box_trad_team = self.nba_client.get_box_scores(game_id_list, 'trad')
        print('Tradititional box scores pulled into objects.')

        print('Creating box_adv_player table if not already exists.')
        # box adv player
        table_name = 'box_adv_player'
        self.create_duckdb_tables(query_string=data_load_strings.create_box_adv_player_table, table=table_name)
        print('Loading data to box_adv_player')
        self.load_data_to_duckdb(
            nba_data=box_adv_players, 
            query_string= data_load_strings.box_adv_player_query_string,
            table=table_name
            )
        
        print('Creating box_adv_team table if not already exists.')
        # box adv team
        table_name = 'box_adv_team'
        self.create_duckdb_tables(query_string=data_load_strings.create_box_adv_team_table, table=table_name)
        print('Loading data to box_adv_team')
        self.load_data_to_duckdb(
            nba_data=box_adv_team, 
            query_string= data_load_strings.box_adv_team_query_string,
            table=table_name
            )
        
        print('Creating box_trad_player table if not already exists.')
        # box trad player
        table_name = 'box_trad_player'
        self.create_duckdb_tables(query_string=data_load_strings.create_box_trad_player_table, table=table_name)
        print('Loading data to box_trad_player')
        self.load_data_to_duckdb(
            nba_data=box_trad_players, 
            query_string= data_load_strings.box_trad_player_query_string,
            table=table_name
            )
        
        print('Creating box_trad_team table if not already exists.')
        # box trad teams
        table_name = 'box_trad_team'
        self.create_duckdb_tables(query_string=data_load_strings.create_box_trad_team_table, table=table_name)
        print('Loading data to box_trad_team')
        self.load_data_to_duckdb(
            nba_data=box_trad_team, 
            query_string= data_load_strings.box_trad_team_query_string,
            table=table_name
            )
