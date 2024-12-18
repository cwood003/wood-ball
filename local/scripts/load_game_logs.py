import duckdb
import polars as pl
from wood_ball.stats.nba_stats import NBA_Stats

stats = NBA_Stats()

game_log_df = pl.DataFrame(stats.get_game_log(date_from="12-10-2024", date_to="12-16-2024"))

con = duckdb.connect('X:/nba_data/my_db.duckdb')

con.sql("""
INSERT OR REPLACE INTO nba_game_log
select * from game_log_df
""")