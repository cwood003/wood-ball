import marimo

__generated_with = "0.10.4"
app = marimo.App(width="medium")


@app.cell
def _():
    # import numpy as np
    # import pandas as pd
    # import requests
    # from basketball_reference_web_scraper import client
    import duckdb
    # import pygwalker
    import polars as pl
    # import plotly
    import marimo as mo
    import wat
    from great_tables import GT, style, loc, google_font
    from wood_ball.library.static.icon_ref import icon_ref
    return GT, duckdb, google_font, icon_ref, loc, mo, pl, style, wat


@app.cell
def _(GT, google_font, loc, style):
    def create_great_table(data, background_color="#f6eee3"):

        polars_result_df = data

        background_color = background_color
        gt = (
            GT(polars_result_df)
            .fmt_image(
                columns="team_icon_path", 
                path="../src/hoop_stats/library/team_images",
                )
            .tab_style(
                style=style.text(color="black", weight='bold'),
                locations=loc.column_labels()
            )
            .tab_style(
                style=style.borders(sides='top', style="dashed"),
                locations = loc.body()
            )
            .opt_table_font(
                font=google_font(name="Montoserrat")
            )
            .tab_options(
                # container_width = "100%",
                table_background_color=background_color,
                # heading_border_bottom_color='black',
                # table_border_top_color ='black',
                column_labels_border_bottom_color='black',
                # column_labels_border_bottom_style="solid",
                # column_labels_border_bottom_width="10px",
                # table_font_style="italic",
                table_border_bottom_color='black'
            )
            # .data_color(
            #     columns="GS",
            #     palette="RdYlGn"
            # )
        )
        return gt
    return (create_great_table,)


@app.cell
def _():
    from nba_api.stats.endpoints import shotchartdetail, commonplayerinfo, teaminfocommon, boxscoreadvancedv2, leaguegamelog, boxscoretraditionalv2
    return (
        boxscoreadvancedv2,
        boxscoretraditionalv2,
        commonplayerinfo,
        leaguegamelog,
        shotchartdetail,
        teaminfocommon,
    )


@app.cell
def _(leaguegamelog):
    game_log = leaguegamelog.LeagueGameLog(
        season_type_all_star="Regular Season",
        date_from_nullable="12-10-2024",
        date_to_nullable="12-10-2024",
    )
    return (game_log,)


@app.cell
def _(game_log, l):
    game_log = game_log.get_normalized_dict()["LeagueGameLog"]
    game_id_list = list(set([game_log['GAME_ID'] for d in l if 'value' in d]))
    # game_id_list = game_log_df.select('GAME_ID').unique()['GAME_ID'].to_list()
    return game_id_list, game_log


@app.cell
def _(game_log_temp, wat):
    wat / game_log_temp
    return


@app.cell
def _():
    # game_id_list = game_log_df.select('GAME_ID').unique()['GAME_ID'].to_list()
    return


@app.cell
def _(boxscoreadvancedv2, boxscoretraditionalv2, game_id_list):
    box_score_advanced_obj_list = [boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id) for game_id in game_id_list]
    trad_box_score_obj_list = [boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id) for game_id in game_id_list]
    return box_score_advanced_obj_list, trad_box_score_obj_list


@app.cell
def _(box_score_advanced_obj_list, pl, trad_box_score_obj_list):
    box_score_player_stats = pl.DataFrame(
        [player_stats for box_score in box_score_advanced_obj_list for player_stats in box_score.get_normalized_dict()["PlayerStats"]]
    )
    box_score_team_stats = pl.DataFrame(
        [player_stats for box_score in box_score_advanced_obj_list for player_stats in box_score.get_normalized_dict()["TeamStats"]]
    )

    trad_box_score_player_stats = pl.DataFrame(
        [player_stats for box_score in trad_box_score_obj_list for player_stats in box_score.get_normalized_dict()["PlayerStats"]]
    )

    trad_box_score_team_stats = pl.DataFrame(
        [player_stats for box_score in trad_box_score_obj_list for player_stats in box_score.get_normalized_dict()["TeamStats"]]
    )
    return (
        box_score_player_stats,
        box_score_team_stats,
        trad_box_score_player_stats,
        trad_box_score_team_stats,
    )


@app.cell
def _(icon_ref, pl):
    png_ref = pl.DataFrame(icon_ref)
    return (png_ref,)


@app.cell
def _(duckdb):
    con = duckdb.connect('X:/nba_data/my_db.duckdb')
    return (con,)


@app.cell
def _(con):
    con.sql("""
    show tables
    """)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        select * from trad_box_score_player_stats

        select * from trad_box_score_team_stats

        select * from box_score_player_stats

        select * from box_score_team_stats
        """
    )
    return


@app.cell
def _(
    box_score_player_stats,
    duckdb,
    game_log_df,
    png_ref,
    trad_player_stats,
):
    pb_rel = duckdb.sql("""
    select adv.game_id, 
    adv.team_id, 
    adv.player_id, 
    adv.team_abbreviation,
    png_ref.team_icon_path,
    adv.player_name,
    gl.game_date,
    gl.matchup,
    gl.WL,
    adv.start_position,
    concat(cast(split_part(adv.min, ':', 1) as double) + (cast(split_part(adv.min, ':', 2) as double) / 60), 2) as MIN_NUMERIC,
    concat(cast(split_part(adv.min, ':', 1) as int), ':', lpad(split_part(adv.min, ':', 2), 2, '0')) as MIN_STRING,
    trad.pts, 
    trad.reb, 
    trad.ast, 
    trad.oreb, 
    trad.to, 
    trad.stl, 
    trad.blk, 
    trad.pf,
    concat(cast(trad.fgm as VARCHAR), '/', cast(trad.fga as VARCHAR)) as FG,
    concat(cast(trad.fg3m as VARCHAR), '/', cast(trad.fg3a as VARCHAR)) as FG_3PT,
    concat(cast(round(usg_pct * 100, 2) as string), '%') as USG_PCT, 
    concat(cast(round(ts_pct * 100, 2) as string), '%') as TS_PCT,
    trad.plus_minus,
    cast(trad.pts + 0.4 * trad.FGM - 0.7 * trad.FGA - 0.4*(trad.FTA - trad.FTM) + 0.7 * trad.OREB + 0.3 * trad.DREB + trad.STL + 0.7 * trad.AST + 0.7 * trad.BLK - 0.4 * trad.PF - trad.TO as double) as GS
    from box_score_player_stats as adv
    join trad_player_stats as trad
    on adv.game_id = trad.game_id and adv.team_id = trad.team_id and adv.player_id = trad.player_id
    join game_log_df as gl
    on gl.team_id = adv.team_id and gl.game_id = adv.game_id
    join png_ref on adv.team_id = png_ref.team_id
    where adv.min is not null
    order by GS desc
    """).pl()

    pb_rel
    return (pb_rel,)


@app.cell
def _(mo, pb_rel):
    final_rel = mo.sql(
        f"""
        select 
            team_icon_path as TEAM,
            player_name as PLAYER,
            MIN_STRING as MIN,
            pts,
            reb, 
            oreb,
            ast,
            "to" as TOV,
            stl,
            blk,
            pf,
            fg,
            fg_3pt,
            usg_pct as USG,
            ts_pct as TS,
            GS
        from pb_rel
        limit 15
        """,
        output=False,
    )
    return (final_rel,)


@app.cell
def _(create_great_table, df):
    create_great_table(df)
    return


if __name__ == "__main__":
    app.run()
