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
    from wood_ball.stats.nba_stats import NBA_Stats
    return (
        GT,
        NBA_Stats,
        duckdb,
        google_font,
        icon_ref,
        loc,
        mo,
        pl,
        style,
        wat,
    )


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        ATTACH 'X:/nba_data/my_db.duckdb' as my_db
        """
    )
    return (my_db,)


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        show all tables
        """
    )
    return


@app.cell
def _(mo, my_db, nba_game_log):
    _df = mo.sql(
        f"""
        select * from my_db.nba_game_log
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        alter table my_db.nba_game_log alter GAME_DATE TYPE DATE
        """
    )
    return


app._unparsable_cell(
    r"""
    create or replace table 
    """,
    name="_"
)


@app.cell
def _(con):
    con.close()
    return


@app.cell
def _(NBA_Stats):
    stats = NBA_Stats()
    return (stats,)


@app.cell
def _(mo, nba_db, nba_game_log):
    game_log_df = mo.sql(
        f"""
        select * from nba_db.nba_game_log
        """
    )
    return (game_log_df,)


@app.cell
def _(game_log_df, pl, stats):
    # this needs to be edited

    game_id_list = game_log_df['GAME_ID'].unique().to_list()

    box_adv_players = pl.DataFrame(stats.get_box_scores(game_id_list, 'adv', 'player'))
    return box_adv_players, game_id_list


@app.cell
def _(box_adv_players, mo):
    _df = mo.sql(
        f"""
        INSERT OR REPLACE INTO my_db.box_adv_player
        select * from box_adv_players
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        show all tables
        """
    )
    return


@app.cell
def _(duckdb):
    con = duckdb.connect('md:?motherduck_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImN3b29kMDEwN0BnbWFpbC5jb20iLCJzZXNzaW9uIjoiY3dvb2QwMTA3LmdtYWlsLmNvbSIsInBhdCI6IkxxVS1PWkV3NUpQLWM5NHNCNmJSNFZDWXhRMUhiM05SNnVHZXFKcWIyczAiLCJ1c2VySWQiOiIwYTMzZGI5OC0xZGY1LTQxY2QtODRkOC0zZDAxNGU5NmFlZTUiLCJpc3MiOiJtZF9wYXQiLCJyZWFkT25seSI6ZmFsc2UsInRva2VuVHlwZSI6InJlYWRfd3JpdGUiLCJpYXQiOjE3MzQ0OTY0MjUsImV4cCI6MTczNDU4MjgyNX0.xPKNWhUiubUdDK6lhD1Ck1YP-OtCn2Z2ioEE7H4HZ78')
    return (con,)


@app.cell
def _(con):
    con.sql("""
        CREATE OR REPLACE DATABASE test_db_2 from current_database(); 
    """)
    return


@app.cell
def _(con, conn):
    con.sql("""
        show all tables; 
    """)

    conn.close()
    return


@app.cell
def _(con):
    con.close()
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE OR REPLACE DATABASE test_1 from current_database();
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        show all tables
        """
    )
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        CREATE DATABASE nba_data from nba_db;
        """
    )
    return


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
def _(game_log_dict, pl):
    pl.DataFrame(game_log_dict)['GAME_ID'].unique().to_list()
    return


@app.cell
def _(trad_box_score_team_stats):
    # polars dataframe schema conversion
    def convert_df_to_duckdb_schema(df):
        ref_dict = {
            'String': "STRING",
            "Float64": "DOUBLE",
            "Int64": "BIGINT"
        }

        for key, value in df.schema.items():
            print((str(key) + ' ' + ref_dict[str(value)] + ','))

    convert_df_to_duckdb_schema(trad_box_score_team_stats)
    return (convert_df_to_duckdb_schema,)


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
