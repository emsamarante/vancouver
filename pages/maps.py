from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from graphs import *
from app import *


df_map0 = pd.read_csv("data/dataset_mapa.csv", index_col=0)
df_store_map = df_map0.to_dict()
df_map = pd.DataFrame(df_store_map)

years = df_map.YEAR.unique()
crimes = sorted(df_map.TYPE.unique())
seasons = sorted(df_map.SEASON.unique())
months = sorted(df_map.MONTH.unique())


all_options = {'years': years, 'crimes': crimes,
               'seasons': seasons, 'months': months}


layout = dbc.Container(children=[
    # Armazenamento de dataset
    dcc.Store(id='dataset_map', data=df_store_map),
    # dcc.Store(id='dataset-fixed', data=df_store),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div(["Choose the year"], style={
                                 "font-size": "80%"}),
                        dcc.Dropdown(
                            id="drop-year",
                            value=2021,
                            options=[{'label': i, 'value': i}
                                     for i in all_options['years']],
                            clearable=False
                        )
                    ])
                ], lg=3),
                dbc.Col([
                    html.Div([
                        html.Div(["Choose the crime"],
                                 style={"font-size": "80%"}),
                        dcc.Dropdown(
                            id="drop-crime",
                            clearable=False
                        )
                    ])
                ], lg=3),
                dbc.Col([
                    html.Div([
                        html.Div(["Choose the season"],
                                 style={"font-size": "80%"}),
                        dcc.Dropdown(
                            id="drop-season",
                            clearable=False
                        )
                    ])
                ], lg=3),
                dbc.Col([
                    html.Div([
                        html.Div(["Choose the month"],
                                 style={"font-size": "80%"}),
                        dcc.Dropdown(
                            id="drop-month",
                            clearable=False
                        )
                    ])
                ], lg=3)
            ], className='g-2 my-auto', style={'margin-top': '9px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H6("Crimes georeferenced"),
                                    dcc.Graph()
                                ])
                            ])
                        ])
                    ], style=tab_card)
                ], lg=8),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H6("Crimes georeferenced"),
                                    dcc.Graph()
                                ])
                            ])
                        ])
                    ], style=tab_card)
                ], lg=4)
            ], className='g-2 my-auto',)
        ]),
    ])
], fluid=True)


@app.callback(
    Output('drop-crime', 'options'),
    [Input('dataset_map', 'data'),
     Input('drop-year', 'value')]
)
def set_crimes_options(data, year):
    df = pd.DataFrame(data)
    crimes = sorted(df[df.YEAR.isin([year])]['TYPE'].unique())
    return [{'label': i, 'value': i} for i in crimes]


@app.callback(
    Output('drop-season', 'options'),
    [Input('dataset_map', 'data'),
     Input('drop-year', 'value'),
     Input('drop-crime', 'value')]
)
def set_season_options(data, year, crime):
    df = pd.DataFrame(data)
    seasons = sorted(df[(df.YEAR.isin([year])) & (
        df.TYPE.isin([crime]))]['SEASON'].unique())
    return [{'label': i, 'value': i} for i in seasons]


@app.callback(
    Output('drop-month', 'options'),
    [Input('dataset_map', 'data'),
     Input('drop-year', 'value'),
     Input('drop-crime', 'value'),
     Input('drop-season', 'value')]
)
def set_month_options(data, year, crime, season):
    df = pd.DataFrame(data)
    months = sorted(df[(df.YEAR.isin([year])) & (df.TYPE.isin([crime])) & (
        df.SEASON.isin([season]))]['MONTH'].unique())
    return [{'label': i, 'value': i} for i in months]
