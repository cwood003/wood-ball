import duckdb
import polars as pl
from wood_ball.stats.nba_stats import NBA_Stats
# from wood_ball.library.static.icon_ref import icon_ref

stats = NBA_Stats()

# con = duckdb.connect('md:?motherduck_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImN3b29kMDEwN0BnbWFpbC5jb20iLCJzZXNzaW9uIjoiY3dvb2QwMTA3LmdtYWlsLmNvbSIsInBhdCI6IkhOVTBDdlBpdVh2VzJqeU80UnExV3RMUm1RN09FVTRybEowanhSV2ZMVDQiLCJ1c2VySWQiOiIwYTMzZGI5OC0xZGY1LTQxY2QtODRkOC0zZDAxNGU5NmFlZTUiLCJpc3MiOiJtZF9wYXQiLCJyZWFkT25seSI6ZmFsc2UsInRva2VuVHlwZSI6InJlYWRfd3JpdGUiLCJpYXQiOjE3MzUzOTkzMDN9.tK3gEbSK3Gpn5YtdIyqYd6ZNA2kMnU-re3Ew-RsgzQQ')
con = duckdb.connect('X:/nba_data/my_db.duckdb')
# this needs to be edited
game_log_df = con.execute(
    """
select * from nba_data.nba_game_log
where GAME_DATE between CAST(? as DATE) and CAST(? as DATE)
""",
    ['2025-01-08', '2025-01-10'], # modify before running for now
).pl()

game_id_list = game_log_df["GAME_ID"].unique().to_list()

box_adv_players, box_adv_team = stats.get_box_scores(game_id_list, 'adv')
box_trad_players, box_trad_team = stats.get_box_scores(game_id_list, 'trad')
# convert to polars_df
box_adv_players_df = pl.DataFrame(box_adv_players)
box_adv_team_df = pl.DataFrame(box_adv_team)

box_trad_players_df = pl.DataFrame(box_trad_players)
box_trad_team_df = pl.DataFrame(box_trad_team)

# box adv player
con.sql("""
INSERT OR REPLACE INTO nba_data.box_adv_player
select GAME_ID,TEAM_ID,TEAM_ABBREVIATION,TEAM_CITY,PLAYER_ID,PLAYER_NAME,NICKNAME,START_POSITION,COMMENT,MIN,E_OFF_RATING,OFF_RATING,E_DEF_RATING,DEF_RATING,E_NET_RATING,NET_RATING,AST_PCT,AST_TOV,AST_RATIO,OREB_PCT,DREB_PCT,REB_PCT,TM_TOV_PCT,EFG_PCT,TS_PCT,USG_PCT,E_USG_PCT,E_PACE,PACE,PACE_PER40,POSS,PIE
from box_adv_players_df
""")

# box adv team
con.sql("""
INSERT OR REPLACE INTO nba_data.box_adv_team
select 
GAME_ID,
    TEAM_ID,
    TEAM_NAME,
    TEAM_ABBREVIATION,
    TEAM_CITY,
    MIN,
    E_OFF_RATING,
    OFF_RATING,
    E_DEF_RATING,
    DEF_RATING,
    E_NET_RATING,
    NET_RATING,
    AST_PCT,
    AST_TOV,
    AST_RATIO,
    OREB_PCT,
    DREB_PCT,
    REB_PCT,
    E_TM_TOV_PCT,
    TM_TOV_PCT,
    EFG_PCT,
    TS_PCT,
    USG_PCT,
    E_USG_PCT,
    E_PACE,
    PACE,
    PACE_PER40,
    POSS,
    PIE
    from box_adv_team_df
""")

# box trad player
con.sql("""
INSERT OR REPLACE INTO nba_data.box_trad_player
select GAME_ID,
    TEAM_ID,
    TEAM_ABBREVIATION,
    TEAM_CITY,
    PLAYER_ID,
    PLAYER_NAME,
    NICKNAME,
    START_POSITION,
    COMMENT,
    MIN,
    FGM,
    FGA,
    FG_PCT,
    FG3M,
    FG3A,
    FG3_PCT,
    FTM,
    FTA,
    FT_PCT,
    OREB,
    DREB,
    REB,
    AST,
    STL,
    BLK,
    "TO" as TOV,
    PF,
    PTS,
    PLUS_MINUS
    from box_trad_players_df
    """)

con.sql("""
INSERT OR REPLACE INTO nba_data.box_trad_team
select 
GAME_ID,
    TEAM_ID,
    TEAM_NAME,
    TEAM_ABBREVIATION,
    TEAM_CITY,
    MIN,
    FGM,
    FGA,
    FG_PCT,
    FG3M,
    FG3A,
    FG3_PCT,
    FTM,
    FTA,
    FT_PCT,
    OREB,
    DREB,
    REB,
    AST,
    STL,
    BLK,
    "TO" as TOV,
    PF,
    PTS,
    PLUS_MINUS
    from box_trad_team_df""")

con.close()