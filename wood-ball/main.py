import typer
from rich import print
from lib.nba_stats import NBA_Stats
from typing_extensions import Annotated as An
from typing import Optional

app = typer.Typer(no_args_is_help=True)

def complete_name():
    return ["Brandon Ingram", "Zion WIlliamson", "Lebron James"]

@app.command()
def hello():
    print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:")

@app.command()
def hex_shot_chart(player_name:  An[str, typer.Argument(help="NBA full player name")] = "Brandon Ingram", season: An[str, typer.Argument(help="NBA Season Name")] = "2023-24"):
    stats = NBA_Stats()
    stats.hex_shot_chart(player_name, season)

if __name__ == "__main__":
    app()