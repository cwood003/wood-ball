import plotly.io as pio
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from lib.draw_plotly_court import draw_plotly_court
import pandas as pd

# this is all assumming we are using the nba_api shot chart detail data
def hex_shot_chart(player_name: str, player_id: str, team_id: str, player_info: dict, bi: pd.DataFrame, league_average: pd.DataFrame, season: str):
    # set gridsize for hexbin calculation
    gridsize = 30
    hex_color = '51, 255, 173,'
    fig_width = 600
    hex_size = 16
    source = 'nba.com/stats'
    left_annotation = 'Cole Wood'

    pio.templates["nba_stats"] = go.layout.Template(
        # LAYOUT
        layout = {
            # Fonts
            # Note - 'family' must be a single string, NOT a list or dict!
            'title':
                {'font': {'family': 'Helvetica Nueue, Helvetica Nueue Light, Sans-serif',
                        'size':24,
                        'color': '#dcdcdc'}
                },
            'font': {'family': 'Helvetica Neue, Helvetica Nueue Light, Sans-serif',
                        'size':12,
                        'color': '#dcdcdc'},
            },
        )

    # cluster by shots attempted
    shots_hex = plt.hexbin(
        bi['LOC_X'], bi['LOC_Y'],
        extent=(-250, 250, 422.5, -47.5), cmap='Blues', gridsize=gridsize)
    plt.close()  # this closes the plot window

    # cluster by shots made
    makes_df = bi[bi['SHOT_MADE_FLAG'] == 1]
    makes_hex = plt.hexbin(
        makes_df['LOC_X'], makes_df['LOC_Y'],
        extent=(-250, 250, 422.5, -47.5), cmap=plt.cm.Reds, gridsize=gridsize)
    plt.close()

    # calculate shot accuracy
    pcts_by_hex = makes_hex.get_array() / shots_hex.get_array()
    pcts_by_hex[np.isnan(pcts_by_hex)] = 0
    # calculate shot count
    shot_count_hex = shots_hex.get_array()
    shot_count_hex[np.isnan(shot_count_hex)] = 0

    # filter out low sample sizes
    filter_threshold = 1
    for i in range(len(pcts_by_hex)):
        if shot_count_hex[i] < filter_threshold:
            pcts_by_hex[i] = 0
            shot_count_hex[i] = 0
    xlocs = [i[0] for i in shots_hex.get_offsets()]
    ylocs = [i[1] for i in shots_hex.get_offsets()]
    accs_by_hex = pcts_by_hex

    # draw plotly chart
    fig = go.Figure()
    draw_plotly_court(fig, fig_width=fig_width)
    fig.add_trace(go.Scatter(
        x=xlocs, y=ylocs, mode='markers', name='markers',
        marker=dict(
            size=hex_size, 
            sizemode='area', 
            color=shot_count_hex,
            colorscale=[
                [0, f'rgba({hex_color} 0.0)'],
                [0.05, f'rgba({hex_color} 0.35)'],
                [0.1, f'rgba({hex_color} 0.4)'],
                [0.2, f'rgba({hex_color} 0.5)'],
                [0.4, f'rgba({hex_color} 0.85)'],
                [0.6, f'rgba({hex_color} 0.9)'],
                [0.8, f'rgba({hex_color} 0.95)'],
                [1, f'rgba({hex_color} 1.0)'],
            ],
            #line=dict(width=1, color='#333333'), 
            symbol='hexagon',
        ),
        text=[f'FGA: {sc}, FG_PCT: {ac}' for sc, ac in zip(shot_count_hex, accs_by_hex)],  # Add this line
    ))
    fig.update_layout(
        template='nba_stats',
        width = 500,
        margin=dict(l=5, r=5, t=80, b=20),
        title={
            'text': f"{player_name} - {player_info['CommonPlayerInfo'][0]['TEAM_ABBREVIATION']}<br><sub>{season} Shot Chart</sub>",
            'y':0.93,  # Adjust this value to move the title up or down
            'x':0.03,
            'xanchor': 'left',
            'yanchor': 'top'},
        paper_bgcolor=' #2f2f2f ',  # Set the color of the paper
        plot_bgcolor=' #2f2f2f ',  # Set the color of the plotting area
        
        annotations=[
            dict(
                x=0.99,
                y=-0.03,
                showarrow=False,
                text=f"source: {source}",
                xref="paper",
                yref="paper",
            ),
            dict(
                x=0.01,
                y=-0.03,
                showarrow=False,
                text=f"{left_annotation}",
                xref="paper",
                yref="paper",
            )
        ]
    )
    fig.update_xaxes(automargin='left+right')
    fig.show(config=dict(displayModeBar=True))