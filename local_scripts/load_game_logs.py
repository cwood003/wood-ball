import duckdb
import polars as pl
from wood_ball.stats.nba_stats import NBA_Stats

stats = NBA_Stats()

game_log_df = pl.DataFrame(stats.get_game_log())

con = duckdb.connect('X:/nba_data/my_db.duckdb')

con.sql("""
create table nba_game_log as
select * from game_log_df
""")