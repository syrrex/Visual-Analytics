from dash import Dash, html, dcc, Input, Output  # pip install dash
import dash_ag_grid as dag  # pip install dash-ag-grid
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

import matplotlib  # pip install matplotlib

matplotlib.use('agg')

# import data
from api import NFLDataAPI

nfl_api = NFLDataAPI()

# # Access df_weeks attribute
df_weeks = nfl_api.df_weeks
df_plays = nfl_api.df_plays
df_games = nfl_api.df_games

# for testing
gameId = 2018090600
playid = 75

information_data = df_plays[(df_plays['gameId'] == gameId) & (df_plays['playId'] == playid)]

random_value_list = df_games["week"].unique()
away_teams = df_games["visitorTeamAbbr"].unique()
home_teams = df_games["homeTeamAbbr"].unique()
gameId_drop = df_games["gameId"]
playid_drop = df_plays["playId"]
quarter_list = [1, 2, 3, 4]

selected_gameId, selected_playId = None, None


scoreA = int(information_data["preSnapHomeScore"].iloc[0])
scoreB = int(information_data["preSnapVisitorScore"].iloc[0])
pass_result = df_plays["passResult"].iloc[0]
TotalDistance = df_plays["yardsToGo"].iloc[0]
YardLine = 0
Hash = 0
Result = 0
Formation = "test"
PlayType = 0
YardsGained = 0

# input for the plot


# ##test plot
# from gamefield import create_football_field


# Convert matplotlib figure to Plotly figure
# plotly_fig = tls.mpl_to_plotly(fig)

##slider infos
# Get the unique play_id values
play_ids = sorted(playid_drop)

# Create evenly spaced integers for the keys
keys = range(len(play_ids))

# Create the marks dictionary
marks = {key: str(play_id) for key, play_id in zip(keys, play_ids)}

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
from gamefield_plotly import animate_play

fig = animate_play(gameId, playid, df_plays, df_weeks)

app.layout = dbc.Container([
    html.H1("American Football Analysis Application", className='mb-2', style={'textAlign': 'center'}),

    dbc.Row([
        dbc.Row([
            dbc.Col([
                html.P("Team A : Team B"),
                html.P(f"{scoreA} : {scoreB}")
            ], width=12),
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='week',
                placeholder='Week',
                clearable=False,
                options=random_value_list),
            dcc.Dropdown(
                id='homeTeam',
                placeholder='Home team',
                clearable=False,
                options=home_teams),
            dcc.Dropdown(
                id='awayTeam',
                placeholder='Away team',
                clearable=False,
                options=away_teams),
            dcc.Dropdown(
                id='down',
                placeholder='Down:',
                clearable=False,
                options=random_value_list),
            dcc.Dropdown(
                id='playType',
                placeholder='Play type',
                clearable=False,
                options=random_value_list),

            dcc.Dropdown(
                id='game_id',
                placeholder='game',
                clearable=False,
                options=gameId_drop),

            dcc.Dropdown(
                id='quarter',
                placeholder='Quarter',
                clearable=False,
                options=quarter_list),

            dcc.Dropdown(
                id='play_id',
                placeholder='play',
                clearable=False,
                disabled=True),

            dbc.Card(
                dbc.CardBody("This is some text within a card body"),
                className="mb-3",
            ),
            dbc.Button("Show", id="showButton", disabled=True,
                       color="primary", className="mr-1", n_clicks=0),
        ], width=4),
        dbc.Col([
            dcc.Graph(id='football-plotly', figure=fig, config={'displayModeBar': False}),
            # not necessary for now
            # dcc.Slider(0, 20, 1, 
            #            value=10,
            #            id="slider"),
            # html.Div(id="slider-output-container"),

            dcc.Slider(
                id='play_id_slider',
                min=min(keys),
                max=max(keys),
                value=min(keys),
                marks={min(keys): str(min(keys)), int(max(keys) / 2): str(int(max(keys) / 2)),
                       max(keys): str(max(keys))},
                tooltip={"placement": "bottom", "template": "Play {value}", "always_visible": True},
                step=1,
            ),
            html.Div(style={'height': '20px'}),  # Add this line before your dbc.Card
            dbc.Card(
                dbc.CardBody(
                    f"Distance Endzone: {TotalDistance}, YardLine: {YardLine}, Hash: {Hash}, Result: {Result}, "
                    f"Offense Formation: {Formation}, PlayType: {PlayType}, YardsGained: {YardsGained}"
                    f"Pass Result: {pass_result}"),
                className="mb-3",
            ),
        ], width=12, md=6),

    ]),

])


# Callback for the Teams
@app.callback(
    Output("homeTeam", "options"),
    Output("homeTeam", "value"),
    Input("week", "value")
)
def update_home_team_dropdown(week):
    if week:
        home_teams = df_games[df_games['week'] == week]['homeTeamAbbr'].unique()
        print(home_teams)
        return [{'label': team, 'value': team} for team in home_teams], None
    # if game_Id:
    #     print(game_Id)
    #     home_teams = df_games[df_games['gameId'] == game_Id]['homeTeamAbbr'].unique()
    #     return [{'label': team, 'value': team} for team in home_teams], home_teams[0]
    else:
        # If no week is selected, disable the home team dropdown and clear its options
        return df_games["homeTeamAbbr"].unique(), None


# @app.callback(
#     Output("homeTeam", "options"),
#     Output("homeTeam", "disabled"),
#     Output("homeTeam", "value"),
#     Input("week", "value"),
#     Input("awayTeam", "value")
# )
# def update_home_team_dropdown(week, away_team):
#     if week:
#         week_data = df_games[df_games['week'] == week]
#         if away_team:
#             home_Team = week_data[week_data["visitorTeamAbbr"] == away_team]["homeTeamAbbr"].iloc[0]
#             return [{'label': home_Team, 'value': home_Team}], False, home_Team
#         else:
#             home_teams = week_data["homeTeamAbbr"].unique()
#             return [{'label': team, 'value': team} for team in home_teams], False, None
#     elif away_team:
#         home_Team = df_games[df_games["visitorTeamAbbr"] == away_team]["homeTeamAbbr"].iloc[0]
#         return [{'label': home_Team, 'value': home_Team}], False, home_Team
#     else:
#         home_teams = df_games["homeTeamAbbr"].unique()
#         return [{'label': team, 'value': team} for team in home_teams], False, None

@app.callback(
    Output("awayTeam", "options"),
    Output("awayTeam", "value"),
    Input("homeTeam", "value"),
    Input("week", "value")
)
def update_away_team_value(selectedHomeTeam, selectedWeek):
    if selectedWeek:
        week_data = df_games[df_games['week'] == selectedWeek]
        if selectedHomeTeam:
            away_team = week_data[week_data["homeTeamAbbr"] == selectedHomeTeam]["visitorTeamAbbr"].iloc[0]
            return [{'label': away_team, 'value': away_team}], away_team
        else:
            away_teams = week_data["visitorTeamAbbr"].unique()
            return [{'label': team, 'value': team} for team in away_teams], None
    elif selectedHomeTeam:
        away_teams = df_games[df_games["homeTeamAbbr"] == selectedHomeTeam]["visitorTeamAbbr"]
        # return [{'label': away_teams, 'value': away_teams}], away_teams
        return [{'label': team, 'value': team} for team in away_teams], None
    else:
        away_teams = df_games["visitorTeamAbbr"].unique()
        return [{'label': team, 'value': team} for team in away_teams], None


# # Callback for the game_id
# @app.callback(
#     Output("game_id", "options"),
#     Output("game_id", "value"),
#     Input("homeTeam", "value"),
#     Input("awayTeam", "value"),
#     Input("week", "value")
# )
# def update_game_id_options(home_team, away_team, week):
#     if home_team and away_team and week:
#         game_id = df_games[(df_games['homeTeamAbbr'] == home_team) & (df_games['visitorTeamAbbr'] == away_team)][
#             "gameId"].unique()
#         return game_id, game_id
#     elif week and not home_team or not away_team:
#         game_id = df_games[df_games['week'] == week]["gameId"].unique()
#         return game_id, None
#     else:
#         return df_games["gameId"].unique(), None


@app.callback(
    Output("game_id", "options"),
    Output("game_id", "value"),
    Input("homeTeam", "value"),
    Input("awayTeam", "value"),
    Input("week", "value")
)
def update_game_id_options(home_team, away_team, week):
    if home_team and away_team and week:
        game_id = df_games[(df_games['homeTeamAbbr'] == home_team) & (df_games['visitorTeamAbbr'] == away_team) & (
                df_games['week'] == week)]["gameId"].unique()
        if len(game_id) > 0:
            return [{'label': id, 'value': id} for id in game_id], game_id[0]
        else:
            return [], None
    elif week:
        game_ids = df_games[df_games['week'] == week]["gameId"].unique()
        return [{'label': id, 'value': id} for id in game_ids], None
    elif home_team:
        game_ids = df_games[df_games["homeTeamAbbr"] == home_team]["gameId"].unique()
        return [{'label': id, 'value': id} for id in game_ids], None
    else:
        return df_games["gameId"].unique(), None


@app.callback(
    Output("showButton", "disabled"),
    Input("week", "value"),
    Input("game_id", "value"),
    Input("homeTeam", "value"),
    Input("awayTeam", "value"),
    Input("quarter", "value")
)
def enable_show_button(week, game_id, home_team, away_team, quarter):
    if week and game_id and home_team and away_team and quarter:
        return False
    else:
        return True


def on_button_click():
    print("Button clicked")


@app.callback(
    Input("game_id", "value"),
    Input("play_id", "value")
)
def update_values(game_id, play_id):
    global selected_gameId, selected_playId
    if game_id:
        selected_gameId = game_id
    if play_id:
        selected_playId = play_id
    print(selected_gameId, selected_playId)


@app.callback(
    # Output("showButton", "children"),
    Input("showButton", "n_clicks")
)
def button_click_callback(n):
    if n is None:
        print("Button not clicked.")
    else:
        on_button_click()
    # Callback for the slider


@app.callback(
    Output("play_id_slider", "min"),
    Output("play_id_slider", "max"),
    Output("play_id_slider", "value"),
    Output("play_id_slider", "marks"),
    Input("game_id", "value")
)
def update_slider(game_id):
    play_id = sorted(df_plays[df_plays['gameId'] == game_id]["playId"].unique())

    play_ids = sorted(play_id)
    # Create evenly spaced integers for the keys
    keys = range(len(play_ids))
    # Create the marks dictionary
    marks = {min(keys): str(min(keys)), int(max(keys) / 2): str(int(max(keys) / 2)), max(keys): str(max(keys))}
    min_value = min(keys)
    max_value = max(keys)
    value = min(keys)
    # marks = {key: str(play_id) for key, play_id in zip(keys, play_ids)}
    return min_value, max_value, value, marks


# Callback for the play_id
@app.callback(
    Output("play_id", "options"),
    Output("play_id", "disabled"),
    Input("game_id", "value"),
    Input("homeTeam", "value"),
    Input("awayTeam", "value"),
    Input("quarter", "value")
)
def update_play_id_options(game_id, home_team, away_team, quarter):
    if game_id and home_team and away_team and quarter:
        return sorted(
            df_plays[(df_plays['gameId'] == game_id) & (df_plays['quarter'] == quarter)]["playId"].unique()), False
        # return sorted(df_plays[df_plays['gameId'] == game_id]["playId"].unique()), False


# Callback for the slider output for plot


# Callback for the plot drop
@app.callback(
    Output("football-plotly", "figure"),
    Output("football-plotly", "config"),
    Input("game_id", "value"),
    Input("play_id", "value")
)
def update_plot(game_id, play_id):
    fig = animate_play(game_id, play_id, df_plays, df_weeks)
    return fig, {'displayModeBar': False}


# # Create interactivity between dropdown component and graph
# @app.callback(
#     Output(component_id='bar-graph-matplotlib', component_property='src'),
#     Output('bar-graph-plotly', 'figure'),
#     Output('grid', 'defaultColDef'),
#     Input('category', 'value'),
# )
# def plot_data(selected_yaxis):
#     # Build the matplotlib figure
#     fig = plt.figure(figsize=(14, 5))
#     plt.bar(df['State'], df[selected_yaxis])
#     plt.ylabel(selected_yaxis)
#     plt.xticks(rotation=30)
#
#     # Save it to a temporary buffer.
#     buf = BytesIO()
#     fig.savefig(buf, format="png")
#     # Embed the result in the html output.
#     fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
#     fig_bar_matplotlib = f'data:image/png;base64,{fig_data}'
#
#     # Build the Plotly figure
#     fig_bar_plotly = px.bar(df, x='State', y=selected_yaxis).update_xaxes(tickangle=330)
#
#     my_cellStyle = {
#         "styleConditions": [
#             {
#                 "condition": f"params.colDef.field == '{selected_yaxis}'",
#                 "style": {"backgroundColor": "#d3d3d3"},
#             },
#             {"condition": f"params.colDef.field != '{selected_yaxis}'",
#              "style": {"color": "black"}
#              },
#         ]
#     }
#
#     return fig_bar_matplotlib, fig_bar_plotly, {'cellStyle': my_cellStyle}


if __name__ == '__main__':
    app.run_server(debug=False, port=8002)
