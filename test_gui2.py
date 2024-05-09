from dash import Dash, html, dcc, Input, Output  # pip install dash
import plotly.express as px
import dash_ag_grid as dag  # pip install dash-ag-grid
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import pandas as pd  # pip install pandas

import matplotlib  # pip install matplotlib

matplotlib.use('agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")
random_value_list = [i for i in range(1, 10)]
scoreA = 5
scoreB = 0
DownDistance = 0
YardLine = 0
Hash = 0
Result = 0
Formation = 0
PlayType = 0
YardsGained = 0

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
            dcc.Graph(id='bar-graph-plotly', figure={}),
            dcc.Slider(0, 20, 1,
                       value=10,
                       id="slider"),
            html.Div(id="slider-output-container"),
            dbc.Card(
                dbc.CardBody(f"Down: {DownDistance}, YardLine: {YardLine}, Hash: {Hash}, Result: {Result}, "
                             f"Formation: {Formation}, PlayType: {PlayType}, YardsGained: {YardsGained}"),
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
