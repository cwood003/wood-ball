import typer
from rich import print
from wood_ball.data_loader.nbacom import NBAComLoader
from typing_extensions import Annotated as An
from typing import Optional
from whenever import Instant, Date, Time

app = typer.Typer(no_args_is_help=True)
load_app = typer.Typer()
app.add_typer(load_app, name="load")
# def complete_name():
#     return ["Brandon Ingram", "Zion WIlliamson", "Lebron James"]


@app.command()
def hello():
    print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:")


@app.command()
def hello_2():
    print("Hello #2, [bold magenta]World[/bold magenta]!", ":vampire:")


@load_app.command("box-scores")
def load_box_scores(
    motherduck_token: An[str, typer.Argument(help="The connection string to your motherduck account and database")] = "",
    local_db_path: An[str, typer.Argument(help="The path to your local duckdb db you would like to use.")] = 'X:/nba_data/my_db.duckdb',
    date_from: An[str, typer.Argument(help="The date FROM which we would like to pull the box scores. Defaults from yesterday.")] = str(Instant.now().to_tz('US/Eastern').date().subtract(days=1)),
    date_to: An[str, typer.Argument(help="The date TO which we would like to pull the box scores. Defaults to today.")] = str(Instant.now().to_tz('US/Eastern').date())
):
    data_loader = NBAComLoader(
        motherduck_token=motherduck_token, local_db_path=local_db_path
    )

    data_loader.load_box_scores(date_from=date_from, date_to=date_to)