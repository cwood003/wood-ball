import duckdb
import polars as pl
from wood_ball.stats.nba_stats import NBA_Stats
# from wood_ball.library.static.icon_ref import icon_ref

stats = NBA_Stats()

con = duckdb.connect('X:/nba_data/my_db.duckdb')

# this needs to be edited
game_log_df = con.execute("""
select * from nba_game_log
where GAME_DATE between ? and ?
""", ["12-10-2024", "12-11-2024"]).pl()

game_id_list = game_log_df['GAME_ID'].unique().to_list()

box_adv_players = pl.DataFrame(stats.get_box_scores(game_id_list, 'adv', 'player'))

con.execute("""
INSERT OR REPLACE INTO ?
select * from box_adv_players
""", ['box_adv_player'])