# Dependencies
from nba_api.stats.endpoints import shotchartdetail, commonplayerinfo, teaminfocommon, boxscoreadvancedv2, leaguegamelog, boxscoretraditionalv2
from nba_api.stats.static import players, teams
import wood_ball.stats.draw_hex_chart as draw_hex_chart
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
import duckdb
from whenever import Instant
from great_tables import GT, style, loc, google_font
from wood_ball.library.static.icon_ref import icon_ref
import polars as pl
from wood_ball.data_loader.nbacom import NBAComLoader
import wood_ball.stats.nba.duckdb_query_strings as duckdb_query_strings

class NBA_Stats:
    """
    A class that provides methods to retrieve NBA player statistics and shot charts.
    """
    def __init__(self, motherduck_token: str = "", local_db_path: str = ':memory:'):
        """
        Initialize the motherduck token and local duckdb path

        Args:
            motherduck_token (str): motherduck token to be used to load data to motherduck
            local_db_path (str, optional): the local duckdb path to load the data to. Defaults to ':memory:' which means all data will be lost when python process is exited.
        """
        
        # self.connection_string
        # print("[dark_orange]<-------NBAComLoader------------------------------->[/dark_orange]")
        # may need to modify this to try except
        self.use_existing_data = False

        if motherduck_token != "":
            self.duck_connection_string = f'md:nba_data?motherduck_token={motherduck_token}'
            self.use_existing_data = True
        elif local_db_path == ':memory:':
            self.duck_connection_string = local_db_path
            print('Using in-memory duckdb database')
        elif local_db_path != ':memory:':
            self.duck_connection_string = local_db_path
            self.use_existing_data = True
            print(f'Using {local_db_path} as duckdb db path')

        self.con = duckdb.connect(f'{self.duck_connection_string}')
    
    def create_great_table(self, data, background_color="#f6eee3"):

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
    
    def best_of_yesterday(
            self, 
            date_from: str = str(Instant.now().to_tz('US/Eastern').date().subtract(days=1)), 
            date_to: str = str(Instant.now().to_tz('US/Eastern').date())
            ):
        """Create best of yesterday great table

        Args:
            date_from (str, optional): _description_. Defaults to yesterday's date ET.
            date_to (str, optional): _description_. Defaults to today's date ET.

        Returns:
            gt: great table
        """ 
        
        png_ref = pl.DataFrame(icon_ref)

        match self.use_existing_data:
            case True:
                pl_df = self.con.execute("""select     
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
                                 from main.best_of_yesterday_prep as boy
                                 join png_ref on boy.team_id = png_ref.team_id
                                 where CAST(GAME_DATE as DATE) between CAST(? as DATE) and CAST(? as DATE)
                                 order by GS desc
                                 limit 25
                                 """, [date_from, date_to]
                                 ).pl()
                return self.create_great_table(pl_df)
            
            case False:
                data_loader = NBAComLoader(duckdb_connection=self.con)
                data_loader.load_box_scores(date_from=date_from, date_to=date_to)

                pl_df = self.con.execute(
                    f""" 
                    with prep as ({duckdb_query_strings.best_of_yesterday_prep})
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
                        USG_PCT as USG,
                        TS_PCT,
                        GS
                        from prep as boy
                        join png_ref on boy.team_id = png_ref.team_id
                        where CAST(GAME_DATE as DATE) between CAST(? as DATE) and CAST(? as DATE)
                        order by GS desc
                        limit 20
                    """, [date_from, date_to]
                ).pl()
                return self.create_great_table(pl_df)


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
        return player_id, player_info.get_normalized_dict()
    
    def get_team_id(self, team_nickname: str) -> str:
        """
        Retrieves the team ID for a given team nickname.

        Args:
            team_nickname (str): The nickname of the team.
        Returns:
            tuple: A tuple containing the team ID and team information.
        """
        team_id = teams.find_teams_by_nickname(team_nickname)[0]["id"]
        return team_id
    
    def get_advanced_box_score(self, game_id):

        return boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id)

    def get_game_log(self, season_type_all_star: str="Regular Season", date_from:str = "12-10-2024",date_to:str = "12-10-2024") -> list[dict]:
        """Get game log for use in other functions

        Args:
            season_type_all_star (str, optional): Need to add the enumeration options. Defaults to "Regular Season".
            date_from (str, optional): Starting date to draw games from, not sure if the date is inclusive or not. Defaults to "12-10-2024".
            date_to (str, optional): Upper bound for the range to draw dates from. Defaults to "12-10-2024".

        Returns:
            _type_: List of dicts for games in the range
        """
        game_log = leaguegamelog.LeagueGameLog(
            season_type_all_star=season_type_all_star,
            date_from_nullable=date_from,
            date_to_nullable=date_to,
        )

        game_log_list = game_log.get_normalized_dict()["LeagueGameLog"]
        return game_log_list


    def get_box_scores(self, game_id_list: list, box_score_type: str = 'adv') -> any:
        """This function pulls box scores from the nba_api and direct from either data.nba.com or stats.nba.com

        Args:
            game_id_list (list): list of game_ids
            box_score_type (str, optional): Box Score type either advanced or traditional. Value options are ['adv', 'trad'].
            box_score_subtype (str, optional): Box score subtype either player or team. Value options are ['player', 'team'].

        Returns:
            Any: will return list of dicts describing the specified box score type
        """
        if box_score_type == 'adv':
            box_score_advanced_obj_list = [boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id) for game_id in game_id_list]
            box_score_team_stats = [player_stats for box_score in box_score_advanced_obj_list for player_stats in box_score.get_normalized_dict()["TeamStats"]]
            box_score_player_stats = [player_stats for box_score in box_score_advanced_obj_list for player_stats in box_score.get_normalized_dict()["PlayerStats"]]
            return box_score_player_stats, box_score_team_stats
        elif box_score_type == 'trad':
            trad_box_score_obj_list = [boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id) for game_id in game_id_list]
            trad_box_score_player_stats = [player_stats for box_score in trad_box_score_obj_list for player_stats in box_score.get_normalized_dict()["PlayerStats"]]
            trad_box_score_team_stats = [player_stats for box_score in trad_box_score_obj_list for player_stats in box_score.get_normalized_dict()["TeamStats"]]
            return trad_box_score_player_stats, trad_box_score_team_stats

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
    
    def hex_shot_chart(self, player_name="Brandon Ingram", team_nickname="Pelicans", season="2023-24"):
        """
        Generates a shot chart for a given player and season using hexagons ala Kirk Goldsberry.

        Args:
            player_name (str, optional): The name of the player. Defaults to "Brandon Ingram".
            season (str, optional): The season year (e.g., "2023-24"). Defaults to "2023-24".
        """
        try:
            player_id, player_info = self.get_player_info(player_name)
            team_id = self.get_team_id(team_nickname)
            
            bi, league_average = self.get_shot_chart(player_id, team_id, season)
            draw_hex_chart.hex_shot_chart(player_name, player_id, team_id, player_info, bi, league_average, season)
        except Exception as e:
            error_message = Text(f"Unable to retrieve player info using {player_name}: {e}", style="bold red")
            console = Console()
            console.print(Panel(error_message, title="Error", border_style="bold red"))