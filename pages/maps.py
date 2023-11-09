from dash import html, dcc, Patch
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from graphs import *
from app import *
import warnings
warnings.filterwarnings("ignore")


df_map0 = pd.read_csv("data/dataset_mapa.csv", index_col=0)
df_store_map = df_map0.to_dict()
df_map = pd.DataFrame(df_store_map)

years = df_map.YEAR.unique()
# crimes = sorted(df_map.TYPE.unique())
# seasons = sorted(df_map.SEASON.unique())
# months = sorted(df_map.MONTH.unique())


# all_options = {'years': years, 'crimes': crimes,
#                'seasons': seasons, 'months': months}


layout = dbc.Container(children=[
    # Armazenamento de dataset
    dcc.Store(id='dataset_map', data=df_store_map),
    # dcc.Store(id='dataset-fixed', data=df_store),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div(([
                        html.Div(["Choose the neighbourhoods"],
                                 style={"font-size": "80%"}),
                        dcc.Input(
                            id='input', type='text',
                            placeholder="Type the initial letter of the neighbourhood names separated by hyphen.",
                            debounce=False,
                            className="form-control"),

                    ])),
                ], lg=4),
                dbc.Col([
                    html.Div([
                        html.Div(["Choose the year"], style={
                                 "font-size": "80%"}),
                        dcc.Dropdown(
                            id="drop-year",
                            value=2021,
                            options=[{'label': i, 'value': i}
                                     for i in years],
                            clearable=False
                        )
                    ])
                ], lg=2),
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
                ], lg=2),
                dbc.Col([
                    html.Div([
                        html.Div(["Choose the season"],
                                 style={"font-size": "80%"}),
                        dcc.Dropdown(
                            id="drop-season",
                            clearable=False
                        )
                    ])
                ], lg=4),
            ], className='g-2 my-auto', style={'margin-top': '9px'}),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H6(
                                                "Percentage of Crimes in Each Season"),
                                            dcc.Graph(id="crimes-season",
                                                      className='scroll',
                                                      figure=fig_bar_season)
                                        ])
                                    ])
                                ])
                            ], style=tab_card),
                            make_tooltip("Relative percentage of crime types by season for each year.",
                                         "crimes-season")
                        ])
                    ], className='g-2 my-auto', style={'margin-top': '9px'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H6(
                                                "Counts of Crimes in Each Season"),
                                            dcc.Graph(id="crimes-season-abs",
                                                      className='scroll',
                                                      figure=fig_bar_season_abs)
                                        ])
                                    ])
                                ])
                            ], style=tab_card),
                            make_tooltip("Total crimes by season for each year.",
                                         "crimes-season-abs")
                        ])
                    ], className='g-2 my-auto', style={'margin-top': '9px'}),
                ], lg=4),
                dbc.Col([
                    dbc.Row([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.H6("Crimes Georeferenced"),
                                        dcc.Graph(id='map')
                                    ])
                                ], className='g-2 my-auto', style={'margin-top': '9px'})
                            ])
                        ], style=tab_card)
                    ], className='g-2 my-auto', style={'margin-top': '9px'})

                ], lg=8)
            ], className='g-2 my-auto',)
        ]),
    ], className='g-2 my-auto', style={'margin-top': '9px'})
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
    Output('map', 'figure'),
    [Input('dataset_map', 'data'),
     Input('drop-year', 'value'),
     Input('drop-crime', 'value'),
     Input('drop-season', 'value'),]
)
def update_map(data, year, crime, season):
    df = pd.DataFrame(data)

    aux = df[(df.YEAR.isin([year])) & (df.TYPE.isin([crime])) & (
        df.SEASON.isin([season]))]

    markers = {1: 'circle',
               2: 'square',
               3: 'diamond',
               4: 'cross',
               5: 'circle',
               6: 'square',
               7: 'diamond',
               8: 'cross',
               9: 'circle',
               10: 'square',
               11: 'diamond',
               12: 'cross',
               }
    aux['markers'] = 'circle'
    aux.loc[:, 'markers'] = aux.MONTH.map(markers)

    fig_map = px.scatter_mapbox(
        aux, lat="Lat", lon="Long", hover_name="TYPE",
        zoom=11, height=710,
        color='MONTH'
    )

    fig_map.update_layout(mapbox_style='carto-darkmatter')
    # fig_map.update_traces(
    #     marker_symbol="square",
    #     selected_marker_size=,
    #     selector=dict(type='scatter'),
    # )
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_map


@cache.memoize(timeout=TIMEOUT)
@app.callback(
    Output('crimes-season', 'figure'),
    [Input('drop-year', 'value'),
     Input('drop-crime', 'value'),
     Input("input", "value"),],
    prevent_initial_call=True
)
def update_graph(year, crime, valor):

    aux = df_map[(df_map.YEAR.isin([year])) & (df_map.TYPE.isin([crime]))]

    Others = aux.NEIGHBOURHOOD.unique()

    if valor:
        lista = []
        letters = valor
        all = letters.split("-")
        for start_letter in all:
            lista += [x for x in Others if x.startswith(start_letter.upper())]

        mask = aux.NEIGHBOURHOOD.isin(lista)

        fig_bar_season = px.histogram(aux[mask].sort_values(['SEASON', 'NEIGHBOURHOOD']),
                                      x="NEIGHBOURHOOD",
                                      color="SEASON",
                                      barnorm="percent",
                                      text_auto=True,
                                      color_discrete_sequence=[
            "#80B912", "#333333", "#626262", "#A0A2A1"],

        )
        fig_bar_season.update_layout(main_config, height=330, yaxis_title="Percent", xaxis_title=None,
                                     )
        # fig_bar_season.update_xaxes(categoryorder='total descending')
        fig_bar_season.update_traces(
            textfont_size=12, textangle=0, cliponaxis=True, texttemplate='%{y:.0f}')

        return fig_bar_season
    else:
        mask = aux.NEIGHBOURHOOD.isin(initial)

        fig_bar_season = px.histogram(aux[mask].sort_values(['SEASON', 'NEIGHBOURHOOD']),
                                      x="NEIGHBOURHOOD",
                                      color="SEASON",
                                      barnorm="percent",
                                      text_auto=True,
                                      color_discrete_sequence=[
            "#80B912", "#333333", "#626262", "#A0A2A1"],

        )
        fig_bar_season.update_layout(main_config, height=330, yaxis_title="Percent", xaxis_title=None,
                                     )
        # fig_bar_season.update_xaxes(categoryorder='total descending',)
        fig_bar_season.update_traces(
            textfont_size=12, textangle=0, cliponaxis=True, texttemplate='%{y:.0f}')

        return fig_bar_season


# px Bar absolute
@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output('crimes-season-abs', 'figure'),
    [Input('drop-year', 'value'),
     Input('drop-crime', 'value'),
     Input("input", "value"),],
    prevent_initial_call=True
)
def update_graph(year, crime, valor):

    aux = df_map[(df_map.YEAR.isin([year])) & (df_map.TYPE.isin([crime]))]

    Others = aux.NEIGHBOURHOOD.unique()

    if valor:
        lista = []
        letters = valor
        all = letters.split("-")
        for start_letter in all:
            lista += [x for x in Others if x.startswith(start_letter.upper())]

        mask = aux.NEIGHBOURHOOD.isin(lista)

        fig_bar_season_abs = px.bar(aux[mask].groupby(['SEASON', 'NEIGHBOURHOOD'])['Lat'].size(
        ).reset_index().rename(columns={"Lat": "Counts"}),
            x='NEIGHBOURHOOD', y='Counts', color='SEASON',
            color_discrete_sequence=[
            "#80B912", "#333333", "#626262", "#A0A2A1"],
        )

        fig_bar_season_abs.update_layout(main_config, height=320, yaxis_title="Counts", xaxis_title=None,
                                         )
        fig_bar_season_abs.update_xaxes(categoryorder='total descending')
        fig_bar_season_abs.update_traces(
            textfont_size=12, textangle=0, cliponaxis=True, texttemplate='%{y:.0f}')

        return fig_bar_season_abs
    else:
        mask = aux.NEIGHBOURHOOD.isin(initial)

        fig_bar_season_abs = px.bar(aux[mask].groupby(['SEASON', 'NEIGHBOURHOOD'])['Lat'].size(
        ).reset_index().rename(columns={"Lat": "Counts"}),
            x='NEIGHBOURHOOD', y='Counts', color='SEASON',
            color_discrete_sequence=[
            "#80B912", "#333333", "#626262", "#A0A2A1"],
        )

        fig_bar_season_abs.update_layout(main_config, height=320, yaxis_title="Counts", xaxis_title=None,
                                         )
        fig_bar_season_abs.update_xaxes(categoryorder='total descending')
        fig_bar_season_abs.update_traces(
            textfont_size=12, textangle=0, cliponaxis=True, texttemplate='%{y:.0f}')

        return fig_bar_season_abs
