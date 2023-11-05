from dash import html, dcc, Patch
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
                            value="Mischief",
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
                                    dcc.Graph(id='map')
                                ])
                            ])
                        ])
                    ], style=tab_card)
                ], lg=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H6("Crimes georeferenced"),
                                    html.Button("Show More", id="new-val"),
                                    dcc.Graph(id="crimes-season",
                                              className='scroll',
                                              figure=fig_bar_season)
                                ])
                            ])
                        ])
                    ], style=tab_card)
                ], lg=6)
            ], className='g-2 my-auto',)
        ]),
    ])
], fluid=True)


@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output('drop-crime', 'options'),
    [Input('dataset_map', 'data'),
     Input('drop-year', 'value')]
)
def set_crimes_options(data, year):
    df = pd.DataFrame(data)
    crimes = sorted(df[df.YEAR.isin([year])]['TYPE'].unique())
    return [{'label': i, 'value': i} for i in crimes]


@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output('drop-season', 'options'),
    [Input('dataset_map', 'data'),
     Input('drop-year', 'value'),
     Input('drop-crime', 'value')],
    prevent_initial_call=True
)
def set_season_options(data, year, crime):
    df = pd.DataFrame(data)
    seasons = sorted(df[(df.YEAR.isin([year])) & (
        df.TYPE.isin([crime]))]['SEASON'].unique())
    return [{'label': i, 'value': i} for i in seasons]


@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output('drop-month', 'options'),
    [Input('dataset_map', 'data'),
     Input('drop-year', 'value'),
     Input('drop-crime', 'value'),
     Input('drop-season', 'value')],
    prevent_initial_call=True

)
def set_month_options(data, year, crime, season):
    df = pd.DataFrame(data)
    months = sorted(df[(df.YEAR.isin([year])) & (df.TYPE.isin([crime])) & (
        df.SEASON.isin([season]))]['MONTH'].unique())
    return [{'label': i, 'value': i} for i in months]


@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output('map', 'figure'),
    [Input('dataset_map', 'data'),
     Input('drop-year', 'value'),
     Input('drop-crime', 'value'),
     Input('drop-season', 'value'),
     Input('drop-month', 'value')]
)
def update_map(data, year, crime, season, month):
    df = pd.DataFrame(data)
    aux = df[(df.YEAR.isin([year])) & (df.TYPE.isin([crime])) & (
        df.SEASON.isin([season])) & (df.MONTH.isin([month]))]

    fig_map = px.scatter_mapbox(
        aux, lat="Lat", lon="Long", hover_name="TYPE", color='NEIGHBOURHOOD', zoom=11, height=700)
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_map


@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output('crimes-season', 'figure'),
    [Input('drop-year', 'value'),
     Input('drop-crime', 'value'),
     Input("new-val", "n_clicks"),],
    prevent_initial_call=True
)
def update_graph(year, crime, n_clicks):
    Others = ['Marpole', 'Mount Pleasant', 'Musqueam',
              'Oakridge', 'Renfrew-Collingwood', 'Riley Park',
              'Shaughnessy', 'South Cambie', 'Stanley Park',
              'Strathcona', 'Sunset', 'Victoria-Fraserview',
              'West End', 'West Point Grey']

    aux = df_map[(df_map.YEAR.isin([year])) & (df_map.TYPE.isin([crime]))]

    others_dict = {}
    for i, value in zip(range(0, len(Others)), Others):
        others_dict[i] = value

    if n_clicks:
        n = n_clicks % len(Others)
        global initial
        initial.append(others_dict[n])
        initial = sorted(initial)
        print(initial)

        if n == 0:
            initial = bairro.copy()

        mask = aux.NEIGHBOURHOOD.isin(initial)

        fig_bar_season = px.histogram(aux[mask].sort_values(['NEIGHBOURHOOD', 'SEASON']),
                                      x="NEIGHBOURHOOD",
                                      color="SEASON",
                                      barnorm="percent",
                                      text_auto=True,

                                      )
        fig_bar_season.update_layout(main_config, height=700, yaxis_title="Percent", xaxis_title=None,
                                     )
        # fig_bar_season.update_xaxes(categoryorder='total descending')
        fig_bar_season.update_traces(
            textfont_size=12, textangle=0, cliponaxis=True, texttemplate='%{y:.0f}')

        return fig_bar_season
    else:
        mask = aux.NEIGHBOURHOOD.isin(bairro)

        fig_bar_season = px.histogram(aux[mask].sort_values(['NEIGHBOURHOOD', 'SEASON']),
                                      x="NEIGHBOURHOOD",
                                      color="SEASON",
                                      barnorm="percent",
                                      text_auto=True,

                                      )
        fig_bar_season.update_layout(main_config, height=700, yaxis_title="Percent", xaxis_title=None,
                                     )
        # fig_bar_season.update_xaxes(categoryorder='total descending')
        fig_bar_season.update_traces(
            textfont_size=12, textangle=0, cliponaxis=True, texttemplate='%{y:.0f}')

        return fig_bar_season
