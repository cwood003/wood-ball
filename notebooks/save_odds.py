import marimo

__generated_with = "0.10.2"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import requests
    from lib.odds import Odds
    import duckdb
    import pygwalker as pg
    return Odds, duckdb, np, pd, pg, requests


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Save NCAA Champ Odds
        """
    )
    return


@app.cell
def _(Odds):
    df = Odds.get_ncaa_champ_odds()
    Odds.append_to_table(df, 'ncaa_champ_odds')
    return (df,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Save NBA Champ Odds
        """
    )
    return


@app.cell
def _(Odds):
    df_1 = Odds.get_nba_champ_odds()
    Odds.append_to_table(df_1, 'nba_champ_odds')
    return (df_1,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Save Todays NBA Game Odds
        """
    )
    return


@app.cell
def _(Odds):
    df_2 = Odds.get_next_24hr_nba_game_odds()
    Odds.append_to_table(df_2, 'nba_game_odds')
    return (df_2,)


@app.cell
def _(df_2, pg):
    pg.walk(df_2, kernel_computation=True)
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()

