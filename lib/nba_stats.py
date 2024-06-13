# Dependencies
from nba_api.stats.endpoints import shotchartdetail, commonplayerinfo
from nba_api.stats.static import players
import lib.draw_hex_chart as draw_hex_chart
from rich.panel import Panel
from rich.text import Text
from rich.console import Console

class NBA_Stats:
    """
    A class that provides methods to retrieve NBA player statistics and shot charts.
    """

    def get_player_info(self, player_name):
        """
        Retrieves the player ID, team ID, and player information for a given player name.

        Args:
            player_name (str): The name of the player.

        Returns:
            tuple: A tuple containing the player ID, team ID, and player information.
        """
        player_id = players.find_players_by_full_name(player_name)[0]["id"]
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        team_id = player_info.get_normalized_dict()['CommonPlayerInfo'][0]['TEAM_ID']
        return player_id, team_id, player_info.get_normalized_dict()

    def get_shot_chart(self, player_id, team_id, year, season_type="Regular Season", context_measure_simple="FGA"):
        """
        Retrieves the shot chart data for a given player, team, and season.

        Args:
            player_id (int): The ID of the player.
            team_id (int): The ID of the team.
            year (str): The season year (e.g., "2023-24").
            season_type (str, optional): The type of season. Defaults to "Regular Season".
            context_measure_simple (str, optional): The measure of context. Defaults to "FGA".

        Returns:
            tuple: A tuple containing the shot chart data and the league average data.
        """
        shot_chart = shotchartdetail.ShotChartDetail(team_id=team_id, player_id=player_id, season_type_all_star="Regular Season",
                                                        season_nullable=year, context_measure_simple="FGA")
        league_average = shot_chart.league_averages.get_data_frame().rename(columns={'FGA': 'FGA_LA', 'FGM': 'FGM_LA', 'FG_PCT': 'FG_PCT_LA'})
        return shot_chart.shot_chart_detail.get_data_frame(), league_average
    
    def hex_shot_chart(self, player_name="Brandon Ingram", season="2023-24"):
        """
        Generates a shot chart for a given player and season using hexagons ala Kirk Goldsberry.

        Args:
            player_name (str, optional): The name of the player. Defaults to "Brandon Ingram".
            season (str, optional): The season year (e.g., "2023-24"). Defaults to "2023-24".
        """
        try:
            player_id, team_id, player_info = self.get_player_info(player_name)
            
            bi, league_average = self.get_shot_chart(player_id, team_id, season)
            draw_hex_chart.hex_shot_chart(player_name, player_id, team_id, player_info, bi, league_average, season)
        except Exception as e:
            error_message = Text(f"Unable to retrieve player info using {player_name}: {e}", style="bold red")
            console = Console()
            console.print(Panel(error_message, title="Error", border_style="bold red"))