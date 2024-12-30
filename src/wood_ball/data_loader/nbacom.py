from wood_ball.stats.nba_stats import NBA_Stats

class NBACom:
    """
    A class that will load nba to users Motherduck account or to a local duckdb of the users choosing
    """
    def __init__(self, motherduck_token: str, local_db_path: str = 'my_duckdb.duckdb'):
        """
        Initialize the motherduck token and local duckdb path

        Args:
            motherduck_token (str): _description_
            local_db_path (str, optional): _description_. Defaults to 'my_duckdb.duckdb'.
        """
        
        self.motherduck_token = motherduck_token
        self.local_db_path = local_db_path

    def load_game_logs(self, date_from:str = "12-10-2024",date_to:str = "12-10-2024"):

        ## add script code here
        
        