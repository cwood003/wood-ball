import marimo

__generated_with = "0.10.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import duckdb
    import polars as pl
    import nba_on_court as noc

    from pathlib import Path
    import marimo as mo
    import nba_on_court as noc
    import pandas as pd
    import numpy as np
    return Path, duckdb, mo, noc, np, pd, pl


@app.cell
def _(noc):
    noc.load_nba_data(seasons=2022, data="nbastats", untar=True)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        select * from 'nbastats_2022.csv'
        """
    )
    return


@app.cell
def _(noc):
    noc.load_nba_data(seasons=2022, data="datanba", untar=True)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        select * from 'datanba_2022.csv'
        """
    )
    return


@app.cell
def _(noc):
    noc.load_nba_data(seasons=2022, data="pbpstats", untar=True)
    return


@app.cell
def _(mo):
    _df = mo.sql(
        f"""
        select * from 'pbpstats_2022.csv'
        """
    )
    return


if __name__ == "__main__":
    app.run()
