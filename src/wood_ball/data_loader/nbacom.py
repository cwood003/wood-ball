from wood_ball.stats.nba_stats import NBA_Stats
import duckdb
import polars
from typing import List, Dict 

class NBACom:
    """
    A class that will load nba to users Motherduck account or to a local duckdb of the users choosing
    """
    def __init__(self, motherduck_token: str = "", local_db_path: str = 'my_duckdb.duckdb'):
        """
        Initialize the motherduck token and local duckdb path

        Args:
            motherduck_token (str): _description_
            local_db_path (str, optional): _description_. Defaults to 'my_duckdb.duckdb'.
        """
        
        self.motherduck_token = motherduck_token
        self.local_db_path = local_db_path
        self.nba_client = NBA_Stats()

        # may need to modify this to try except
        if motherduck_token != "":
            self.con = con = duckdb.connect(f'md:?motherduck_token={motherduck_token}')
        elif local_db_path == 'my_duckdb.duckdb':
            print('Using Current Directory to write duckdb db')
            self.con = con = duckdb.connect(f'{local_db_path}')
        elif local_db_path != 'my_duckdb.duckdb':
            print(f'Using {local_db_path} as duckdb db path')
            self.con = con = duckdb.connect(f'{local_db_path}')

    def load_game_logs(self, nba_data: List[Dict[any, any]], database: str = 'nba_data', table: str = 'game_log'):

        self.con.execute("""
        INSERT OR REPLACE INTO ?
        select SEASON_ID,TEAM_ID,TEAM_ABBREVIATION,TEAM_NAME,GAME_ID,GAME_DATE,MATCHUP,WL,MIN,FGM,FGA,FG_PCT,
        FG3M,FG3A,FG3_PCT,FTM,FTA,FT_PCT,OREB,DREB,REB,AST,STL,BLK,TOV,PF,PTS,PLUS_MINUS,VIDEO_AVAILABLE
        from ?
            """, [database, table])
        
    def load_box_scores(self)
