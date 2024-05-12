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

gameId = 2018090600
playid = 75

information_data = df_plays[(df_plays['gameId'] == gameId) & (df_plays['playId'] == playid)]


random_value_list = [i for i in range(1, 10)]
scoreA = int(information_data["preSnapHomeScore"].iloc[0])
scoreB = int(information_data["preSnapVisitorScore"].iloc[0])
pass_result = df_plays["passResult"].iloc[0]       
TotalDistance = df_plays["yardsToGo"].iloc[0]
YardLine = 0
Hash = 0
Result = 0
Formation = test
PlayType = 0
YardsGained = 0


#input for the plot


# ##test plot
# from gamefield import create_football_field
from gamefield_plotly import animate_play

# def gamefield():
#     train = pd.read_csv('data/train.csv', low_memory=False)
#     fig, ax = create_football_field()
#     train.query("PlayId == 20170907000118 and Team == 'away'") \
#             .plot(x='X', y='Y', kind='scatter', ax=ax, color='orange', s=30, legend='Away')
#     train.query("PlayId == 20170907000118 and Team == 'home'") \
#             .plot(x='X', y='Y', kind='scatter', ax=ax, color='blue', s=30, legend='Home')
#     plt.title('Play # 20170907000118')
#     plt.legend()
#     return fig

fig = animate_play(gameId, playid)

# Convert matplotlib figure to Plotly figure
#plotly_fig = tls.mpl_to_plotly(fig)



app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
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
                options=random_value_list),
            dcc.Dropdown(
                id='awayTeam',
                placeholder='Away team',
                clearable=False,
                options=random_value_list),
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
            dbc.Card(
                dbc.CardBody("This is some text within a card body"),
                className="mb-3",
            ),
            dbc.Button("Show", disabled=True, color="primary", className="mr-1"),
        ], width=4),
        dbc.Col([
            dcc.Graph(id='bar-graph-plotly', figure=fig),
            #not necessary for now
            # dcc.Slider(0, 20, 1, 
            #            value=10,
            #            id="slider"),
            # html.Div(id="slider-output-container"),
            dbc.Card(
                dbc.CardBody(f"Distance Endzone: {TotalDistance}, YardLine: {YardLine}, Hash: {Hash}, Result: {Result}, "
                             f"Offense Formation: {Formation}, PlayType: {PlayType}, YardsGained: {YardsGained}"
                             f"Pass Result: {pass_result}"),
                className="mb-3",
            ),
        ], width=12, md=6),

    ]),

])

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
