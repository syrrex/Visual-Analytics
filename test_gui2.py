from dash import Dash, html, dcc, Input, Output  # pip install dash
import plotly.express as px
import dash_ag_grid as dag  # pip install dash-ag-grid
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import pandas as pd  # pip install pandas

import matplotlib  # pip install matplotlib


matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import base64
from io import BytesIO

import plotly.tools as tls

# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")
# #import data
from api import NFLDataAPI
nfl_api = NFLDataAPI()

# # Access df_weeks attribute
df_weeks = nfl_api.df_weeks
df_plays = nfl_api.df_plays
df_games = nfl_api.df_games

#for testing
gameId = 2018090600
playid = 75

information_data = df_plays[(df_plays['gameId'] == gameId) & (df_plays['playId'] == playid)]


random_value_list = [i for i in range(1, 10)]
away_teams = df_games["visitorTeamAbbr"].unique()
home_teams = df_games["homeTeamAbbr"].unique()
gameId_drop = df_games["gameId"]
playid_drop = df_plays["playId"]

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


#input for the plot


# ##test plot
# from gamefield import create_football_field


# Convert matplotlib figure to Plotly figure
#plotly_fig = tls.mpl_to_plotly(fig)

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
                id='quarter',
                placeholder='Quarter',
                clearable=False,
                options=random_value_list),

            dcc.Dropdown(
                id='game_id',
                placeholder='game',
                clearable=False,
                options=gameId_drop),

            dcc.Dropdown(
                id='play_id',
                placeholder='play',
                clearable=False,
                options=playid_drop),


            dbc.Card(
                dbc.CardBody("This is some text within a card body"),
                className="mb-3",
            ),
            dbc.Button("Show", disabled=True, color="primary", className="mr-1"),
        ], width=4),
        dbc.Col([
            dcc.Graph(id='football-plotly', figure=fig, config={'displayModeBar': False}),
            #not necessary for now
            # dcc.Slider(0, 20, 1, 
            #            value=10,
            #            id="slider"),
            # html.Div(id="slider-output-container"),
            
            dcc.Slider(
            id='play_id_slider',
            min=min(keys),
            max=max(keys),
            value=min(keys),
            marks={min(keys): str(min(keys)), int(max(keys)/2): str(int(max(keys)/2)), max(keys): str(max(keys))},
            tooltip={"placement": "bottom","template": "Play {value}", "always_visible": True},
            step=1,
            ),
            html.Div(style={'height': '20px'}),  # Add this line before your dbc.Card
            dbc.Card(
                dbc.CardBody(f"Distance Endzone: {TotalDistance}, YardLine: {YardLine}, Hash: {Hash}, Result: {Result}, "
                             f"Offense Formation: {Formation}, PlayType: {PlayType}, YardsGained: {YardsGained}"
                             f"Pass Result: {pass_result}"),
                className="mb-3",
            ),
        ], width=12, md=6),

    ]),

])

# Callback for the Teams
@app.callback(
    Output("awayTeam", "options"),
    Input("homeTeam", "value")
)
def update_away_team_options(home_team):
    away_teams = df_games[df_games['homeTeamAbbr'] == home_team]['visitorTeamAbbr'].unique()
    return away_teams

# Callback for the game_id
@app.callback(
    Output("game_id", "options"),
    Input("homeTeam", "value"),
    Input("awayTeam", "value")
)
def update_game_id_options(home_team, away_team):
    game_id = df_games[(df_games['homeTeamAbbr'] == home_team) & (df_games['visitorTeamAbbr'] == away_team)]["gameId"].unique()
    return game_id

#Callback for the slider
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
    marks = {min(keys): str(min(keys)), int(max(keys)/2): str(int(max(keys)/2)), max(keys): str(max(keys))}
    min_value = min(keys)
    max_value = max(keys)
    value = min(keys)
    #marks = {key: str(play_id) for key, play_id in zip(keys, play_ids)}
    return min_value, max_value, value, marks

# Callback for the play_id
@app.callback(
    Output("play_id", "options"),
    Input("game_id", "value")
)
def update_play_id_options(game_id):
    play_id = df_plays[df_plays['gameId'] == game_id]["playId"].unique()
    return play_id

#Callback for the slider output for plot


#Callback for the plot drop
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
