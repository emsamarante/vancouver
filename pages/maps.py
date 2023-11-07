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
                                     for i in all_options['years']],
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
                                            # html.Div(([
                                            #     html.Div(["Choose the neighbourhoods"],
                                            #              style={"font-size": "80%"}),
                                            #     dcc.Input(
                                            #         id='input', type='text',
                                            #         placeholder="Type the initial letter of the neighbourhood names separated by hyphen.",
                                            #         debounce=False,
                                            #         className="form-control"),

                                            # ])),
                                            html.H6(
                                                "Percentage of Crimes in Each Season"),
                                            dcc.Graph(id="crimes-season",
                                                      className='scroll',
                                                      figure=fig_bar_season_abs)
                                        ])
                                    ])
                                ])
                            ], style=tab_card)
                        ])
                    ], className='g-2 my-auto', style={'margin-top': '9px'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H6(
                                                "Percentage of Crimes in Each Season"),
                                            dcc.Graph(id="crimes-season-abs",
                                                      className='scroll',
                                                      figure=fig_bar_season)
                                        ])
                                    ])
                                ])
                            ], style=tab_card)
                        ])
                    ], className='g-2 my-auto', style={'margin-top': '9px'}),
                ], lg=4),
                dbc.Col([
                    dbc.Row([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.H6("Crimes georeferenced"),
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


# @cache.memoize(timeout=TIMEOUT)  # in seconds
# @app.callback(
#     Output('drop-month', 'options'),
#     [Input('dataset_map', 'data'),
#      Input('drop-year', 'value'),
#      Input('drop-crime', 'value'),
#      Input('drop-season', 'value')],
#     prevent_initial_call=True

# )
# def set_month_options(data, year, crime, season):
#     df = pd.DataFrame(data)
#     months = sorted(df[(df.YEAR.isin([year])) & (df.TYPE.isin([crime])) & (
#         df.SEASON.isin([season]))]['MONTH'].unique())
#     return [{'label': i, 'value': i} for i in months]


@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output('map', 'figure'),
    [Input('dataset_map', 'data'),
     Input('drop-year', 'value'),
     Input('drop-crime', 'value'),
     Input('drop-season', 'value'),]
    #  Input('drop-month', 'value'),],
)
def update_map(data, year, crime, season):
    df = pd.DataFrame(data)

    # aux = df[(df.YEAR.isin([year])) & (df.TYPE.isin([crime])) & (
    #     df.SEASON.isin([season])) & (df.MONTH.isin([month]))]
    aux = df[(df.YEAR.isin([year])) & (df.TYPE.isin([crime])) & (
        df.SEASON.isin([season]))]

    # discrete_colors = ["blue", "green", "red", "purple", "orange"]
    # colors_dict = {}
    # num_months = aux.MONTH.nunique()
    # months = aux.MONTH.unique()
    # count = 0
    # print(f"{num_months} e {months}")
    # # while count <= num_months:
    # #     colors_dict[months[count]] = discrete_colors[count]
    # #     count += 1

    fig_map = px.scatter_mapbox(
        aux, lat="Lat", lon="Long", hover_name="TYPE",
        color='MONTH', zoom=11, height=700,
        color_discrete_map=None)
    fig_map.update_layout(mapbox_style='carto-darkmatter')
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig_map


@cache.memoize(timeout=TIMEOUT)  # in seconds
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

        lista = sorted(lista)

        mask = aux.NEIGHBOURHOOD.isin(lista)

        fig_bar_season = px.histogram(aux[mask].sort_values(['NEIGHBOURHOOD', 'SEASON']),
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

        fig_bar_season = px.histogram(aux[mask].sort_values(['NEIGHBOURHOOD', 'SEASON']),
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

        lista = sorted(lista)

        mask = aux.NEIGHBOURHOOD.isin(lista)

        fig_bar_season_abs = px.bar(aux[mask].groupby(['NEIGHBOURHOOD', 'SEASON'])['Lat'].size(
        ).reset_index().rename(columns={"Lat": "Counts"}),
            x='NEIGHBOURHOOD', y='Counts', color='SEASON',
            color_discrete_sequence=[
            "#80B912", "#333333", "#626262", "#A0A2A1"])

        fig_bar_season_abs.update_layout(main_config, height=320, yaxis_title="Counts", xaxis_title=None,
                                         )
        # fig_bar_season.update_xaxes(categoryorder='total descending')
        fig_bar_season_abs.update_traces(
            textfont_size=12, textangle=0, cliponaxis=True, texttemplate='%{y:.0f}')

        return fig_bar_season_abs
    else:
        mask = aux.NEIGHBOURHOOD.isin(initial)

        fig_bar_season_abs = px.bar(aux[mask].groupby(['NEIGHBOURHOOD', 'SEASON'])['Lat'].size(
        ).reset_index().rename(columns={"Lat": "Counts"}),
            x='NEIGHBOURHOOD', y='Counts', color='SEASON',
            color_discrete_sequence=[
            "#80B912", "#333333", "#626262", "#A0A2A1"])

        fig_bar_season_abs.update_layout(main_config, height=320, yaxis_title="Counts", xaxis_title=None,
                                         )
        # fig_bar_season.update_xaxes(categoryorder='total descending')
        fig_bar_season_abs.update_traces(
            textfont_size=12, textangle=0, cliponaxis=True, texttemplate='%{y:.0f}')

        return fig_bar_season_abs
