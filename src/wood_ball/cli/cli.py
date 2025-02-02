import typer
from rich import print
from wood_ball.data_loader.nbacom import NBAComLoader
from wood_ball.stats.nba.nba_stats import NBA_Stats
from typing_extensions import Annotated as An
from typing import Optional
from whenever import Instant, Date, Time

app = typer.Typer(no_args_is_help=True,
                  help="""
                  The wood-ball cli tool was initally created for dev work but it is set up to be used \n
                  as a tool where the default behavior is to save the data to an in memory duckdb database that will hang out\n
                  as long as the python session is active.\n\n

                  You can set the tool to read/write from motherduck or to a local duckdb.\n
                  I would recommend setting the following Env Variables: 'DUCKDB_PATH' or 'MOTHERDUCK_TOKEN'
                  """
                  )
load_app = typer.Typer()
viz_app = typer.Typer()
app.add_typer(load_app, name="load")
app.add_typer(viz_app, name='viz')

@load_app.command("box-scores")
def load_box_scores(
    motherduck_token: An[str, typer.Option(envvar="MOTHERDUCK_TOKEN", help="The connection string to your motherduck account and database")] = "",
    local_db_path: An[str, typer.Argument(envvar="DUCKDB_PATH", help="The path to your local duckdb db you would like to use.")] = ':memory:',
    date_from: An[str, typer.Option(help="The date FROM which we would like to pull the box scores. Defaults from yesterday.")] = str(Instant.now().to_tz('US/Eastern').date().subtract(days=1)),
    date_to: An[str, typer.Option(help="The date TO which we would like to pull the box scores. Defaults to today.")] = str(Instant.now().to_tz('US/Eastern').date())
):
    """Load box scores to duckdb
    """
    data_loader = NBAComLoader(
        motherduck_token=motherduck_token, local_db_path=local_db_path
    )

    data_loader.load_box_scores(date_from=date_from, date_to=date_to)

@viz_app.command("boy")
def display_best_of_yesterday_table(
    motherduck_token: An[str, typer.Option(envvar="MOTHERDUCK_TOKEN", help="The connection string to your motherduck account and database")] = "",
    local_db_path: An[str, typer.Argument(envvar="DUCKDB_PATH", help="The path to your local duckdb db you would like to use.")] = ':memory:',
    # date_from: An[str, typer.Option(help="The date FROM which we would like to pull the box scores. Defaults from yesterday.")] = str(Instant.now().to_tz('US/Eastern').date().subtract(days=1)),
    # date_to: An[str, typer.Option(help="The date TO which we would like to pull the box scores. Defaults to today.")] = str(Instant.now().to_tz('US/Eastern').date())
):
    """Load box scores to duckdb and display best of yesterday viz for yesterday only
    """
    stats = NBA_Stats()
    stats.best_of_yesterday().show()