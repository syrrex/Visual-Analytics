import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Example usage
#gameId_example = 2018090600  # Replace with actual gameId
#playId_example = 75  # Replace with actual playId
#displayName_example = 'Matt Ryan'  # Replace with the actual player's name

def speed_acc_plot_interactive(df_weeks, gameId, playId):
    # Assuming df_weeks is your DataFrame and is already loaded
    gameId_example = gameId
    playId_example = playId

    # Filter the DataFrame
    filtered_df = df_weeks[(df_weeks['gameId'] == gameId_example) & (df_weeks['playId'] == playId_example)]

    # Unique list of players
    players = filtered_df['displayName'].unique()

    # Create a subplot
    fig = make_subplots(rows=1, cols=1)

    # Initial plot for the first player (as default)
    default_player = players[0]
    default_df = filtered_df[filtered_df['displayName'] == default_player]
    fig.add_trace(
        go.Scatter(x=default_df['time'], y=default_df['s'], name='Speed', mode='lines+markers', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=default_df['time'], y=default_df['a'], name='Acceleration', mode='lines+markers',
                             line=dict(color='blue')))

    # Create a dropdown menu for player selection
    buttons = []
    for player in players:
        player_df = filtered_df[filtered_df['displayName'] == player]
        buttons.append(dict(
            args=[{
                "x": [player_df['time'], player_df['time']],
                "y": [player_df['s'], player_df['a']],
            }],
            label=str(player),
            method="update"
        ))

    fig.update_layout(
        updatemenus=[dict(
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=-0.25,  # Adjust this value to move the dropdown more to the left
            xanchor="left",
            y=1.1,
            yanchor="top"
        )]
    )

    # Update layout to add titles and make it more informative
    fig.update_layout(title_text="Player Speed and Acceleration Over Time", xaxis_title="Time",
                      yaxis_title="Yards/Second")
    fig.add_layout_image(
        dict(
            source="https://upload.wikimedia.org/wikipedia/de/1/12/National_Football_League_2008.svg",
            # Replace with the actual URL or path
            xref="paper", yref="paper",
            x=1, y=1,
            sizex=0.04, sizey=0.2,  # Adjust size to fit the corner
            sizing="stretch",
            opacity=1,
            layer="above",
            xanchor="right", yanchor="top"
        )
    )
    # Show the figure
    return fig


def distance_heatmap(df_weeks, gameId, playId):
    filtered_df = df_weeks[(df_weeks['gameId'] == gameId) & (df_weeks['playId'] == playId)]

    player_ids = filtered_df['displayName'].unique()
    frames = filtered_df['frameId'].unique()
    frames.sort()  # Ensure frames are in order

    fig = make_subplots(rows=1, cols=1)
    frames_list = []

    colorscale = [
        [0.0, 'white'],  # transition through white
        [1.0, 'red']  # end with red
    ]

    for frame in frames:
        frame_df = filtered_df[filtered_df['frameId'] == frame]
        num_players = frame_df['displayName'].nunique()
        distance_matrix = np.zeros((num_players, num_players))

        for i, player_id1 in enumerate(player_ids):
            for j, player_id2 in enumerate(player_ids):
                if i < j:
                    player1 = frame_df[frame_df['displayName'] == player_id1].iloc[0]
                    player2 = frame_df[frame_df['displayName'] == player_id2].iloc[0]
                    distance = np.sqrt((player1['x'] - player2['x']) ** 2 + (player1['y'] - player2['y']) ** 2)
                    distance_matrix[i, j] = distance
                    distance_matrix[j, i] = distance  # Symmetric

        interaction_threshold = 20  # Example threshold
        interaction_matrix = np.where(distance_matrix < interaction_threshold, distance_matrix, np.nan)

        heatmap = go.Heatmap(
            z=interaction_matrix,
            x=player_ids.tolist(),
            y=player_ids.tolist(),
            colorscale=colorscale,  # Use the custom colorscale
            showscale=True,
            colorbar=dict(
                title='Distance',
                titleside='right',
                tickmode='array',
                tickvals=[0, 5, 10, 15, 20, 25, 30],
                ticks='outside'
            )
        )

        frame_trace = go.Frame(data=[heatmap], name=f'frame{frame}')
        frames_list.append(frame_trace)

    fig.frames = frames_list

    # Initial data
    fig.add_trace(go.Heatmap(
        z=frames_list[0].data[0].z,
        x=player_ids.tolist(),
        y=player_ids.tolist(),
        colorscale=colorscale,  # Use the custom colorscale
        showscale=True,
        colorbar=dict(
            title='Distance',
            titleside='right',
            tickmode='array',
            tickvals=[0, 5, 10, 15, 20, 25, 30],
            ticks='outside'
        )
    ), 1, 1)

    # Dropdown setup
    dropdown_buttons = [
        {
            'label': f'Frame {frame}',
            'method': 'animate',
            'args': [
                [f'frame{frame}'],
                {'frame': {'duration': 300, 'redraw': True},
                 'mode': 'immediate',
                 'transition': {'duration': 300}}
            ]
        } for frame in frames
    ]

    fig.update_layout(
        updatemenus=[
            {
                'buttons': dropdown_buttons,
                'direction': 'down',
                'pad': {'r': 10, 't': 10},
                'showactive': True,
                'x': -0.25,
                'xanchor': 'left',
                'y': 1.15,
                'yanchor': 'top'
            }
        ],
        title='Player Interaction Heatmap Based on Proximity',
    )

    return fig
