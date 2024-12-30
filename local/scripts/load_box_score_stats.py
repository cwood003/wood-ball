import duckdb
import polars as pl
from wood_ball.stats.nba_stats import NBA_Stats
# from wood_ball.library.static.icon_ref import icon_ref

stats = NBA_Stats()

con = con = duckdb.connect('md:?motherduck_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImN3b29kMDEwN0BnbWFpbC5jb20iLCJzZXNzaW9uIjoiY3dvb2QwMTA3LmdtYWlsLmNvbSIsInBhdCI6IkhOVTBDdlBpdVh2VzJqeU80UnExV3RMUm1RN09FVTRybEowanhSV2ZMVDQiLCJ1c2VySWQiOiIwYTMzZGI5OC0xZGY1LTQxY2QtODRkOC0zZDAxNGU5NmFlZTUiLCJpc3MiOiJtZF9wYXQiLCJyZWFkT25seSI6ZmFsc2UsInRva2VuVHlwZSI6InJlYWRfd3JpdGUiLCJpYXQiOjE3MzUzOTkzMDN9.tK3gEbSK3Gpn5YtdIyqYd6ZNA2kMnU-re3Ew-RsgzQQ')

# this needs to be edited
game_log_df = con.execute(
    """
select * from nba_game_log
where GAME_DATE between ? and ?
""",
    ["12-10-2024", "12-11-2024"],
).pl()

game_id_list = game_log_df["GAME_ID"].unique().to_list()
box_adv_players = pl.DataFrame(stats.get_box_scores(game_id_list, "adv", "player"))

con.execute(
    """
INSERT OR REPLACE INTO ?
select * from box_adv_players
""",
    ["box_adv_player"],
)

stats.get_box_scores()