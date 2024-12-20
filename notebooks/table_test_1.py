import marimo

__generated_with = "0.10.2"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import requests
    # from basketball_reference_web_scraper import client
    import duckdb
    import pygwalker
    import polars as pl
    import plotly
    from reactable import Reactable, embed_css
    return (
        Reactable,
        duckdb,
        embed_css,
        np,
        pd,
        pl,
        plotly,
        pygwalker,
        requests,
    )


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
def _(boxscoretraditionalv2, pl):
    trad_box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id='0022401203').get_normalized_dict()

    trad_player_stats = pl.DataFrame(trad_box_score['PlayerStats'])
    trad_team_stats = pl.DataFrame(trad_box_score['TeamStats'])
    trade_team_starter_bench_stats = pl.DataFrame(trad_box_score['TeamStarterBenchStats'])
    return (
        trad_box_score,
        trad_player_stats,
        trad_team_stats,
        trade_team_starter_bench_stats,
    )


@app.cell
def _(boxscoreadvancedv2, leaguegamelog, pl):
    game_log = leaguegamelog.LeagueGameLog(season_type_all_star='Regular Season', date_from_nullable='12-10-2024', date_to_nullable='12-11-2024')
    game_log_df = pl.DataFrame(game_log.get_normalized_dict()['LeagueGameLog'])

    box_score = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id='0022401203')
    box_score_player_stats = pl.DataFrame(box_score.get_normalized_dict()['PlayerStats'])
    box_score_team_stats = pl.DataFrame(box_score.get_normalized_dict()['TeamStats'])
    return (
        box_score,
        box_score_player_stats,
        box_score_team_stats,
        game_log,
        game_log_df,
    )


@app.cell
def _(pl):
    team_name_ref = [{
        "team_id": '1610612742',
        "team_icon_path": 'Mavericks.png'
        },
        {"team_id": "1610612760", "team_icon_path": 'Thunder.png'}
        ]

    png_ref = pl.DataFrame(team_name_ref)
    return png_ref, team_name_ref


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
    round(cast(split_part(adv.min, ':', 1) as double) + (cast(split_part(adv.min, ':', 2) as double) / 60), 2) as min,
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
    usg_pct, 
    ts_pct, 
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
    limit 8
    """).pl()

    # final_rel = duckdb.sql("""

    # """)
    return (pb_rel,)


@app.cell
def _(Reactable, embed_css, pb_rel):
    embed_css()

    Reactable(
        pb_rel,
        default_page_size=5,
        searchable=True,
        filterable=True,
    )
    return


@app.cell
def _(pb_rel):
    from great_tables import GT
    background_color = "#333333"
    logo_size = '0.01'
    gt = (
        GT(pb_rel)
        .fmt_image(
            columns="team_icon_path", 
            path="../src/hoop_stats/library/team_images",
            height=logo_size,
            width=logo_size
            )
        # .tab_header(
        #     title="The Best of Yesterday Test",
        #     subtitle="The best players sorted by game score"
        #     )
        .tab_options(
            # container_width = "100%",
            table_background_color=background_color,
            column_labels_border_top_color=background_color,
            column_labels_border_bottom_style="solid",
            # column_labels_border_bottom_width="10px",
            # table_font_style="italic",
            table_font_names="Liberation Mono"
        )
    )

    gt
    return GT, background_color, gt, logo_size


@app.cell
def _():
    # td = TidyTable()

    # cmap = td.cmap
    # col_def_dict = {
    #     "date": {"textprops": {"ha": "left", "weight": "bold"}, "width": 1},
    #     "team": {"textprops": {"ha": "left", "weight": "bold"}, "width": 2},
    #     "opponent": {"group": "Matchup Info", "textprops": {"ha": "center"}, "width": 2},
    #     "outcome": {"group": "Matchup Info", "textprops": {"ha": "center"}, "width": 0.75},
    #     "active": {"group": "Matchup Info", "textprops": {"ha": "center"}, "width": 0.75},
    #     "plus_minus": {
    #         "group": "Stats",
    #         "textprops": {"ha": "center"},
    #         "width": 0.75,
    #         "border": "left",
    #         # Assuming `normed_cmap`, `test_df`, `cmap`, and `num_stds` are defined elsewhere
    #         "cmap": normed_cmap(test_df['plus_minus'], cmap=cmap, num_stds=2.5)
    #     },
    # }
    return


@app.cell
def _(TidyTable, df, normed_cmap, test_df):
    td = TidyTable()

    cmap =td.cmap

    col_def_dict = {
        "name": {"textprops": {"ha": "left", "weight": "bold"}, "width": 1},
        "team": {"textprops": {"ha": "left", "weight": "bold"}, "width": 2},
        "opponent": {"group": "Matchup Info", "textprops": {"ha": "center"}, "width": 2},
        "outcome": {"group": "Matchup Info", "textprops": {"ha": "center"}, "width": 0.75},
        "active": {"group": "Matchup Info", "textprops": {"ha": "center"}, "width": 0.75},
        "plus_minus": {
            "group": "Stats",
            "textprops": {"ha": "center"},
            "width": 0.75,
            "border": "left",
            # Assuming `normed_cmap`, `test_df`, `cmap`, and `num_stds` are defined elsewhere
            "cmap": normed_cmap(test_df['plus_minus'], cmap=cmap, num_stds=2.5)
        },
    }

    td.create_table(date=df, col_def_dict=col_def_dict)
    return cmap, col_def_dict, td


if __name__ == "__main__":
    app.run()