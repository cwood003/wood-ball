import duckdb
import polars as pl
from wood_ball.stats.nba_stats import NBA_Stats

stats = NBA_Stats()

game_log_df = pl.DataFrame(stats.get_game_log(date_from="01-08-2025", date_to="01-10-2025"))

con = duckdb.connect('X:/nba_data/my_db.duckdb')

con.sql("""
INSERT OR REPLACE INTO nba_data.nba_game_log
select * from game_log_df
""")

con.close()