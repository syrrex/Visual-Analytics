from dash import Dash, html, dcc, Input, Output  # pip install dash
import dash_ag_grid as dag  # pip install dash-ag-grid
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import dash

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
buttonClicked = 0
downslist = df_plays["down"].unique()

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
teamA = df_games["homeTeamAbbr"].iloc[0]
teamB = df_games["visitorTeamAbbr"].iloc[0]
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

from additionalplots import calculate_acceleration
from additionalplots import speed_acc_plot_interactive
from additionalplots import distance_heatmap

fig = animate_play(gameId, playid, df_plays, df_weeks)

speed_fig = speed_acc_plot_interactive(df_weeks, gameId, playid)
distance_fig = distance_heatmap(df_weeks, gameId, playid)


app.layout = dbc.Container([
    html.H1("American Football Analysis Application", className='mb-2', style={'textAlign': 'center'}),

    dbc.Row([
        dbc.Row([
            dbc.Col([
                html.P(f"{teamA} : {teamB}", id= "teams"),
                html.P(f"{scoreA} : {scoreB}", id= "score")
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
                id='game_id',
                placeholder='game',
                clearable=False,
                options=gameId_drop, disabled=True),
            dcc.Dropdown(
                id='down',
                placeholder='Down:',
                clearable=False,
                options=downslist),

            #dcc.Dropdown(
                #id='playType',
                #placeholder='Play type',
                #clearable=False,
                #options=random_value_list),

            dcc.Dropdown(
                id='quarter',
                placeholder='Quarter',
                clearable=False,
                disabled=True,
                options=quarter_list),

            dcc.Dropdown(
                id='play_id',
                placeholder='play',
                clearable=False,
                disabled=True),

            dbc.Card(
                dbc.CardBody("This is some text within a card body"),
                className="mb-3",
                id="cardInfo"
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

            
            html.Div(style={'height': '20px'}),  # Add this line before your dbc.Card
            dbc.Card(
                dbc.CardBody(
                    f"Distance Endzone: {TotalDistance}, YardLine: {YardLine}, Hash: {Hash}, Result: {Result}, "
                    f"Offense Formation: {Formation}, PlayType: {PlayType}, YardsGained: {YardsGained}"
                    f"Pass Result: {pass_result}"),
                className="mb-3",
                id="additionalInfo"
            ),
        ], width=12, md=6),
        dbc.Col([
            dcc.Graph(id='speed-plot', figure=speed_fig, config={'displayModeBar': False}),

            dcc.Graph(id='distance-heatmap', figure=distance_fig, config={'displayModeBar': False}),

    ], width=10),

]) ])


# Callback for the week
@app.callback(
    Output("week", "options"),
    Output("week", "value"),
    Input("week", "value"),
    Input("game_id", "value"),
    Input("homeTeam", "value"),
    Input("awayTeam", "value")
)
def update_game_id_options(selectedWeek, selectedGame, selectedHome, selectedAway):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger = 'None'
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Here Week")
    print(trigger)
    if trigger == "week":
        return [{'label': week, 'value': week} for week in random_value_list], selectedWeek
    if trigger == "game_id":
        week = df_games[df_games["gameId"] == selectedGame]["week"].iloc[0]
        return [{'label': week, 'value': week} for week in random_value_list], week
    if trigger == "homeTeam" or trigger == "awayTeam":
        if selectedHome and selectedAway:
            week = df_games[(df_games["homeTeamAbbr"] == selectedHome) & (df_games["visitorTeamAbbr"] == selectedAway)][
                "week"].iloc[0]
            return [{'label': week, 'value': week} for week in random_value_list], week


# Callback for the Teams
@app.callback(
    Output("homeTeam", "options"),
    Output("homeTeam", "value"),
    Input("game_id", "value"),
    Input("week", "value"),
    Input("awayTeam", "value"),
    Input("homeTeam", "value")
)
def update_home_team_dropdown(selectedGame, selectedWeek, selectedAway, selectedHome):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger = 'None'
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Here Home")
    print("Trigger: ", trigger)
    if trigger == "week":
        week_data = df_games[df_games['week'] == selectedWeek]
        options = week_data["homeTeamAbbr"].unique()
        return [{'label': team, 'value': team} for team in options], None
    if trigger == "game_id":
        home_team = df_games[df_games["gameId"] == selectedGame]["homeTeamAbbr"].iloc[0]
        options = df_games["homeTeamAbbr"].unique()
        return [{'label': team, 'value': team} for team in options], home_team
    if trigger == "awayTeam":
        if selectedWeek:
            home_team = df_games[(df_games["visitorTeamAbbr"] == selectedAway) & (df_games["week"] == selectedWeek)][
                "homeTeamAbbr"].iloc[0]
            options = df_games["homeTeamAbbr"].unique()
            return [{'label': team, 'value': team} for team in options], home_team
    if trigger == "homeTeam":
        week_data = df_games[df_games['week'] == selectedWeek]
        options = week_data["homeTeamAbbr"].unique()
        return [{'label': team, 'value': team} for team in options], selectedHome

    # if selectedGame and not selectedWeek and not selectedAway:
    #     home_team = df_games[df_games["gameId"] == selectedGame]["homeTeamAbbr"].iloc[0]
    #     options = df_games["homeTeamAbbr"].unique()
    #     return [{'label': team, 'value': team} for team in options], home_team
    # if selectedWeek:
    #     week_data = df_games[df_games['week'] == selectedWeek]
    #     if selectedAway:
    #         home_team = week_data[week_data["visitorTeamAbbr"] == selectedAway]["homeTeamAbbr"].iloc[0]
    #         options = week_data["homeTeamAbbr"].unique()
    #         return [{'label': team, 'value': team} for team in options], home_team
    #     else:
    #         options = week_data["homeTeamAbbr"].unique()
    #         if selectedHome:
    #             return [{'label': team, 'value': team} for team in options], selectedHome
    #         return [{'label': team, 'value': team} for team in options], None
    # elif selectedAway:
    #     options = df_games[df_games["visitorTeamAbbr"] == selectedAway]["homeTeamAbbr"].unique()
    #     if selectedHome:
    #         return [{'label': team, 'value': team} for team in options], selectedHome
    #     return [{'label': team, 'value': team} for team in options], None
    # else:
    #     options = df_games["homeTeamAbbr"].unique()
    #     if selectedHome:
    #         return [{'label': team, 'value': team} for team in options], selectedHome
    #     return [{'label': team, 'value': team} for team in options], None

@app.callback(
    Output("awayTeam", "options"),
    Output("awayTeam", "value"),
    Input("homeTeam", "value"),
    Input("week", "value"),
    Input("awayTeam", "value"),
    Input("game_id", "value")
)
def update_away_team_value(selectedHomeTeam, selectedWeek, selectedAway, selectedGame):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger = 'None'
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Here Away")
    print("Trigger: ", trigger)
    if trigger == "homeTeam":
        if selectedWeek:
            away_team = df_games[(df_games["homeTeamAbbr"] == selectedHomeTeam) & (df_games["week"] == selectedWeek)][
                "visitorTeamAbbr"].iloc[0]
            options = df_games["visitorTeamAbbr"].unique()
            return [{'label': team, 'value': team} for team in options], away_team
        
    if trigger == "week":
        week_data = df_games[df_games['week'] == selectedWeek]
        options = week_data["visitorTeamAbbr"].unique()
        return [{'label': team, 'value': team} for team in options], None
    if trigger == "awayTeam":
        options = df_games["visitorTeamAbbr"].unique()
        return [{'label': team, 'value': team} for team in options], selectedAway
    if trigger == "game_id":
        away_team = df_games[df_games["gameId"] == selectedGame]["visitorTeamAbbr"].iloc[0]
        options = df_games["visitorTeamAbbr"].unique()
        return [{'label': team, 'value': team} for team in options], away_team

    #
    # if selectedWeek:
    #     week_data = df_games[df_games['week'] == selectedWeek]
    #     if selectedHomeTeam:
    #         away_team = week_data[week_data["homeTeamAbbr"] == selectedHomeTeam]["visitorTeamAbbr"].iloc[0]
    #         options = week_data["visitorTeamAbbr"].unique()
    #         return [{'label': team, 'value': team} for team in options], away_team
    #     else:
    #         options = week_data["visitorTeamAbbr"].unique()
    #         if selectedAway:
    #             return [{'label': team, 'value': team} for team in options], selectedAway
    #         return [{'label': team, 'value': team} for team in options], None
    # elif selectedHomeTeam:
    #     options = df_games[df_games["homeTeamAbbr"] == selectedHomeTeam]["visitorTeamAbbr"]
    #     if selectedAway:
    #         return [{'label': team, 'value': team} for team in options], selectedAway
    #     return [{'label': team, 'value': team} for team in options], None
    # else:
    #     options = df_games["visitorTeamAbbr"].unique()
    #     if selectedAway:
    #         return [{'label': team, 'value': team} for team in options], selectedAway
    #     return [{'label': team, 'value': team} for team in options], None


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
    Input("week", "value"),
    Input("game_id", "value")
)
def update_game_id_options(selectedHome, selectedAway, selectedWeek, selectedGame):
    ctx = dash.callback_context
    if not ctx.triggered:
        trigger = 'None'
    else:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    print("Here Game")
    print("Trigger: ", trigger)
    if trigger == "homeTeam" or trigger == "awayTeam":
        if selectedHome and selectedAway:
            game_id = df_games[(df_games['homeTeamAbbr'] == selectedHome) & (df_games['visitorTeamAbbr'] == selectedAway)][
                "gameId"].unique()
            options = df_games["gameId"].unique()
            return [{'label': id, 'value': id} for id in options], game_id[0]
    if trigger == "week":
        game_ids = df_games[df_games['week'] == selectedWeek]["gameId"].unique()
        return [{'label': id, 'value': id} for id in game_ids], None
    if trigger == "game_id":
        options = df_games["gameId"].unique()
        return [{'label': id, 'value': id} for id in options], selectedGame


    # if home_team and away_team and week:
    #     game_id = df_games[(df_games['homeTeamAbbr'] == home_team) & (df_games['visitorTeamAbbr'] == away_team) & (
    #             df_games['week'] == week)]["gameId"].unique()
    #     if len(game_id) > 0:
    #         return [{'label': id, 'value': id} for id in game_id], game_id[0]
    #     else:
    #         return [], None
    # elif week:
    #     game_ids = df_games[df_games['week'] == week]["gameId"].unique()
    #     return [{'label': id, 'value': id} for id in game_ids], None
    # elif home_team:
    #     game_ids = df_games[df_games["homeTeamAbbr"] == home_team]["gameId"].unique()
    #     return [{'label': id, 'value': id} for id in game_ids], None
    # else:
    #     return df_games["gameId"].unique(), None


@app.callback(
    Output("showButton", "disabled"),
    Input("week", "value"),
    Input("game_id", "value"),
    Input("homeTeam", "value"),
    Input("awayTeam", "value"),
    Input("quarter", "value")
)
def enable_show_button(week, game_id, home_team, away_team, quarter):
    return not week or not game_id or not home_team or not away_team or not quarter
    # if week and game_id and home_team and away_team and quarter:
    #     return False
    # else:
    #     return True


def on_button_click():
    print("Button clicked")


def update_plot(game_id, play_id):
    fig = animate_play(game_id, play_id, df_plays, df_weeks)
    return fig, {'displayModeBar': False}


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

@app.callback(
    Output("quarter", "options"),
    Output("quarter", "value"),
    Output("quarter", "disabled"),
    Input("game_id", "value"),
    Input("quarter", "value")
)
def update_quarter_options(selectedGame, selectedQuarter):
    if selectedGame:
        return quarter_list, selectedQuarter, False
    else:
        return [], None, True


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
    else:
        return [], True

@app.callback(
    Output("cardInfo", "children"),
    Input("game_id", "value"),
    Input("play_id", "value")
)
def update_card_info(game_id, play_id):
    text = "No information available."
    if game_id and play_id:
        information_data = df_plays[(df_plays['gameId'] == game_id) & (df_plays['playId'] == play_id)]
        print(information_data.columns)
        yardsToGo = information_data["yardsToGo"].iloc[0]
        down = information_data["down"].iloc[0]
        playType = information_data["playType"].iloc[0].split("_")[2]
        playDescription = information_data["playDescription"].iloc[0]
        text = f"Down: {down}, Yards to go: {yardsToGo}, Play Type: {playType}, Play Description: {playDescription}"

    return dbc.CardBody(text)

@app.callback(
    Output("additionalInfo", "children"),
    Input("game_id", "value"),
    Input("play_id", "value")
)
def update_card_adinfo(game_id, play_id):
    text = "No information available."
    if game_id and play_id:
        information_data = df_plays[(df_plays['gameId'] == game_id) & (df_plays['playId'] == play_id)]
        print(information_data.columns)
        yardlinen = information_data["yardlineNumber"].iloc[0]
        yardsToGo = information_data["yardsToGo"].iloc[0]
        playResult = information_data["playResult"].iloc[0]
        Formation = information_data["offenseFormation"].iloc[0]
        PlayType = information_data["playType"].iloc[0]
        pass_result = information_data["passResult"].iloc[0]
        text = f"Distance first down: {yardsToGo}, YardLine: {yardlinen}, Net yards gained: {playResult}, Offense Formation: {Formation}, PlayType: {PlayType}, Pass Result: {pass_result}"

    return dbc.CardBody(text)

@app.callback(
    Output("football-plotly", "figure"),
    Output("football-plotly", "config"),
    Output("speed-plot", "figure"),
    Output("distance-heatmap", "figure"),
    Output("score", "children"),
    Output("teams", "children"),
    Input("showButton", "n_clicks"),
    Input("game_id", "value"),
    Input("play_id", "value"),
    Input("homeTeam", "value"),
    Input("awayTeam", "value")
)
def button_click_callback(n, game_id, play_id, homeTeam, awayTeam):
    global buttonClicked
    if n is None:
        print("Button not clicked.")
    else:
        print(f"Button clicked.{n}")
        if n > buttonClicked:
            buttonClicked = n

            on_button_click()
            fig = animate_play(game_id, play_id, df_plays, df_weeks)
            speed_fig = speed_acc_plot_interactive(df_weeks, game_id, play_id)
            distance_fig = distance_heatmap(df_weeks, game_id, play_id)
            home_score = int(df_plays[(df_plays['gameId'] == game_id) & (df_plays['playId'] == play_id)]["preSnapHomeScore"].iloc[0])
            away_score = int(df_plays[(df_plays['gameId'] == game_id) & (df_plays['playId'] == play_id)]["preSnapVisitorScore"].iloc[0])
            hometeam = homeTeam
            awayteam = awayTeam
            return fig, {'displayModeBar': False}, speed_fig, distance_fig, f"{home_score} : {away_score}", f"{hometeam} : {awayteam}"
        # return update_plot(game_id, play_id)
    # Callback for the slider


# Callback for the slider output for plot


# Callback for the plot drop
# @app.callback(
#     Output("football-plotly", "figure"),
#     Output("football-plotly", "config"),
#     Input("game_id", "value"),
#     Input("play_id", "value")
# )
# def update_plot(game_id, play_id):
#     fig = animate_play(game_id, play_id, df_plays, df_weeks)
#     return fig, {'displayModeBar': False}


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
