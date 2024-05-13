import plotly.graph_objects as go
import numpy as np
import pandas as pd

def animate_play(gameId, playId):
    # Read data from CSV
    data = pd.read_csv('data/plays.csv', low_memory=False)
    data1 = pd.read_csv('data/week1.csv', low_memory=False)
    
    # Filter data for the specific gameId and playId
    play_data = data1[(data1['gameId'] == gameId) & (data1['playId'] == playId)]
    information_data = data[(data['gameId'] == gameId) & (data['playId'] == playId)]
    
    
    # Sample data for demonstration
    line_of_scrimmage = information_data.iloc[0]['absoluteYardlineNumber']
    first_down_marker = information_data.iloc[0]['absoluteYardlineNumber'] + information_data.iloc[0]['yardsToGo']
    down = information_data.iloc[0]['down']
    quarter = information_data.iloc[0]['quarter']
    gameClock = information_data.iloc[0]['gameClock']
    playDescription = "Sample Play Description"

    # initialize plotly start and stop buttons for animation
    updatemenus_dict = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 100, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 0}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]
    # initialize plotly slider to show frame position in animation
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Frame:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 400, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    #frames
#frames
    frames = []
    for frameId in range(1, len(pd.unique(play_data['frameId']))):  # Adjust the range according to your data
        frame_data_home = []
        frame_data_away = []
        frame_data_football = []
        for _, player in play_data[play_data['frameId'] == frameId].iterrows():
            # Players with team colors and jersey numbers
            x_val, y_val = player['x'], player['y']  # Get player coordinates
            if player["displayName"] == "Football":
                player_info = "Football"
            else:
                player_info = f"{player['displayName']} ({int(player['jerseyNumber'])})"  # Player info for legend

            if player['team'] == 'away':
                team_color = 'blue'  # Assign team color
                frame_data_away.append(
                    go.Scatter(
                        x=[x_val], 
                        y=[y_val], 
                        mode='markers+text',  # Added '+text' back here
                        marker=go.scatter.Marker(
                            color=team_color,
                            size=23,  # Increase dot size
                            line=dict(width=2, color='Black'),
                            opacity=0.8
                        ),
                        text=[str(int((player['jerseyNumber'])))],  # Display jersey number
                        textfont=dict(
                            family="Courier New, monospace",
                            size=13,  # Increase font size
                            color="white",
                            weight="bold"
                        ),
                        name=player_info,  # Display player info in the legend
                        hoverinfo='text'
                    )
                )
            elif player['team'] == 'home':
                team_color = 'red'  # Assign team color
                frame_data_home.append(
                    go.Scatter(
                        x=[x_val], 
                        y=[y_val], 
                        mode='markers+text',  # Added '+text' back here
                        marker=go.scatter.Marker(
                            color=team_color,
                            size=23,  # Increase dot size
                            line=dict(width=2, color='Black'),
                            opacity=0.8
                        ),
                        text=[str(int((player['jerseyNumber'])))],  # Display jersey number
                        textfont=dict(
                            family="Courier New, monospace",
                            size=13,  # Increase font size
                            color="white",
                            weight="bold"
                        ),
                        name=player_info,  # Display player info in the legend
                        hoverinfo='text'
                    )
                )
            else:  # Football
                team_color = "brown"  # Assign team color
                player_info = "Football"
                frame_data_football.append(
                    go.Scatter(
                        x=[x_val], 
                        y=[y_val], 
                        mode='markers+text',  # Added '+text' back here
                        marker=go.scatter.Marker(
                            color=team_color,
                            size=18,  # Increase dot size
                            line=dict(width=2, color='White')
                        ),
                        text=[str("F")],  # Display jersey number
                        textfont=dict(
                            family="Courier New, monospace",
                            size=13,  # Increase font size
                            color="white",
                            weight="bold"
                        ),
                        name=player_info,  # Display player info in the legend
                        hoverinfo='text'
                    )
                )
        frame_data = frame_data_home + frame_data_away + frame_data_football
        frames.append(go.Frame(data=frame_data, name=str(frameId)))

        # add frame to slider
        slider_step = {"args": [
            [frameId],
            {"frame": {"duration": 100, "redraw": False},
            "mode": "immediate",
            "transition": {"duration": 0}}
        ],
            "label": str(frameId),
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)
        frames.append(go.Frame(data=frame_data, name=str(frameId)))




    #information for figure
    scale = 10
    layout = go.Layout(
        autosize=False,
        width=120 * scale,
        height=60 * scale,
        xaxis=dict(range=[0, 120], autorange=False, tickmode='array', tickvals=np.arange(10, 111, 5).tolist(),
                showticklabels=False),
        yaxis=dict(range=[0, 53.3], autorange=False, showgrid=False, showticklabels=False),

        plot_bgcolor='#00B140',
        # Create title and add play description at the bottom of the chart for better visual appeal
        title=dict(
            text=f"GameId: {gameId}, PlayId: {playId}<br>{gameClock} {quarter}Q" + "<br>" * 19 + f"{playDescription}",
            x=0.5,  # Center the title
            font=dict(
                size=24,  # Increase font size
                color='black',
                family='Courier New, monospace',
                weight='bold'  # Make the title bold
            )
        ),
        updatemenus=updatemenus_dict,
        sliders=[sliders_dict],
        legend=dict(
            x=1.02,
            y=1,
            traceorder='normal',
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(255, 255, 255, 0.5)',
            borderwidth=1,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="black"
            )
    )
)



    fig = go.Figure(
        data=frames[0]["data"],
        layout=layout,
        frames=frames[1:]
    )
    # Create First Down Markers 
    for y_val in [0, 53]:
        fig.add_annotation(
            x=first_down_marker,
            y=y_val,
            text=str(down),
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="black"
            ),
            align="center",
            bordercolor="black",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=1
        )
    #line of scrimamage
    fig.add_vline(x=line_of_scrimmage, line_width=4, line_dash="dash", line_color="red", opacity=0.7)

    # Add First down line 
    fig.add_vline(x=first_down_marker, line_width=4, line_dash="dash", line_color="yellow", opacity=0.7)

    #add numbers on field
    fig.add_trace(
    go.Scatter(
        x=np.arange(20, 110, 10), 
        y=[5] * len(np.arange(20, 110, 10)),
        mode='text',
        text=list(map(str, list(np.arange(20, 61, 10) - 10) + list(np.arange(40, 9, -10)))),
        textfont=dict(
            size=30,
            family="Courier New, monospace",
            color="#ffffff"
        ),
        showlegend=False,
        hoverinfo='none'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=np.arange(20, 110, 10), 
            y=[53.5 - 5] * len(np.arange(20, 110, 10)),
            mode='text',
            text=list(map(str, list(np.arange(20, 61, 10) - 10) + list(np.arange(40, 9, -10)))),
            textfont=dict(
                size=30,
                family="Courier New, monospace",
                color="#ffffff"
            ),
            showlegend=False,
            hoverinfo='none'
        )
    )

    # Add Endzone Colors 
    endzone_colors = ['#4B0082', '#4B0082']  # purple endzone
    for i, x_min in enumerate([0, 110]):
        fig.add_trace(
            go.Scatter(
                x=[x_min, x_min, x_min + 10, x_min + 10, x_min],
                y=[0, 53.5, 53.5, 0, 0],
                fill="toself",
                fillcolor=endzone_colors[i],
                mode="lines",
                line=dict(
                    color="white",
                    width=3
                ),
                opacity=0.5,
                showlegend=False,
                hoverinfo="skip"
            )
        )


    # Add Team Abbreviations in EndZone's
    for x_min in [0, 110]:
        if x_min == 0:
            angle = 270
            teamName = "Home"
        else:
            angle = 90
            teamName = "Visitor"
        fig.add_annotation(
            x=x_min + 5,
            y=53.5 / 2,
            text=teamName,
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=32,
                color="White"
            ),
            textangle=angle
        )
    return fig