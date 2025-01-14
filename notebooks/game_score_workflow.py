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
    from pathlib import Path
    import polars as pl
    import plotly
    import marimo as mo
    import wat
    from great_tables import GT, style, loc, google_font
    from wood_ball.library.static.icon_ref import icon_ref
    from wood_ball.stats.nba_stats import NBA_Stats
    from wood_ball.data_loader.nbacom import NBAComLoader, data_load_strings
    return (
        GT,
        NBAComLoader,
        NBA_Stats,
        Path,
        data_load_strings,
        duckdb,
        google_font,
        icon_ref,
        loc,
        mo,
        pl,
        plotly,
        style,
        wat,
    )


@app.cell
def _(NBAComLoader):
    data_loader = NBAComLoader(local_db_path='X:/nba_data/my_db.duckdb')
    return (data_loader,)


@app.cell
def _(data_loader):
    data_loader.con.sql('show all tables')
    return


@app.cell
def _(data_load_strings, data_loader):
    data_loader.create_duckdb_tables(query_string=data_load_strings.create_nba_game_log_table, table='nba_game_log')
    return


@app.cell
def _(data_loader):
    data_loader.load_box_scores(date_from='2025-01-13', date_to='2025-01-14')
    return


@app.cell
def _(data_loader):
    del data_loader.con
    return


@app.cell
def _(data_load_strings, data_loader):
    database = 'nba_data'
    table = 'nba_game_log'
    query = data_load_strings.create_nba_game_log_table
    data_loader.con.execute(f"""
        CREATE TABLE IF NOT EXISTS {database}.{table} (
        {query}
        )
    """)
    return database, query, table


@app.cell
def _(data_load_strings, data_loader):
    data_loader.create_duckdb_tables(query_string=data_load_strings.create_nba_game_log_table, table='nba_game_log')
    return


@app.cell
def _(GT, google_font, loc, style):
    def create_great_table(data, background_color="#f6eee3"):

        polars_result_df = data

        background_color = background_color
        gt = (
            GT(polars_result_df)
            .fmt_image(
                columns="TEAM", 
                path="src/wood_ball/library/team_images",
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
def _(icon_ref, pl):
    png_ref = pl.DataFrame(icon_ref)
    return (png_ref,)


@app.cell
def _(con):
    pb_rel = con.sql("""
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
    trad.TOV, 
    trad.stl, 
    trad.blk, 
    trad.pf,
    concat(cast(trad.fgm as VARCHAR), '/', cast(trad.fga as VARCHAR)) as FG,
    concat(cast(trad.fg3m as VARCHAR), '/', cast(trad.fg3a as VARCHAR)) as FG_3PT,
    concat(cast(round(usg_pct * 100, 2) as string), '%') as USG_PCT, 
    concat(cast(round(ts_pct * 100, 2) as string), '%') as TS_PCT,
    trad.plus_minus,
    cast(trad.pts + 0.4 * trad.FGM - 0.7 * trad.FGA - 0.4*(trad.FTA - trad.FTM) + 0.7 * trad.OREB + 0.3 * trad.DREB + trad.STL + 0.7 * trad.AST + 0.7 * trad.BLK - 0.4 * trad.PF - trad.TOV as double) as GS
    from nba_data.box_adv_player as adv
    join nba_data.box_trad_player as trad
    on adv.game_id = trad.game_id and adv.team_id = trad.team_id and adv.player_id = trad.player_id
    join nba_data.nba_game_log as gl
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
            game_date,
            matchup,
            pts,
            reb, 
            oreb,
            ast,
            TOV,
            stl,
            blk,
            pf,
            fg,
            fg_3pt,
            usg_pct as USG,
            ts_pct as TS,
            GS
        from pb_rel
        order by GS desc
        limit 15
        """,
        output=False,
    )
    return (final_rel,)


@app.cell
def _(final_rel):
    final_rel.limit(10)
    return


@app.cell
def _(create_great_table, final_rel):
    create_great_table(final_rel.limit(11))
    return


if __name__ == "__main__":
    app.run()
