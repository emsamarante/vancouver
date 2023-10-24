from dash import html, dcc, Patch
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from dash_bootstrap_templates import ThemeSwitchAIO
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from graphs import *
# from graphs import aux_bar

import time

from app import *


texto = """ Vancouver is one of the most ethnically and linguistically diverse cities in Canada: 49.3 percent of its residents are
 not native English speakers, 47.8 percent are native speakers of neither English nor French, and 54.5 percent of residents belong 
 to visible minority groups. It has been consistently ranked one of the most livable cities in Canada and in the world.
 In terms of housing affordability, Vancouver is also one of the most expensive cities in Canada and in the world.
 Vancouver plans to become the greenest city in the world. Vancouverism is the city's urban planning design philosophy. """


texto_project_1 = """ Not all areas of Vancouver are as safe as others. Vancouver has been been voted one of the best cities in the 
world to live in, but crime statistics clearly indicate that there are some areas where you want to have your wits about you. These areas are often 
referred to as "hot spots" of crime. """

texto_project_2 = """In this project I analyse data of crimes in Vancouver and show the results in the attractive way. This dashboard is compound
by four screens: """


# # ================================ data
# df = pd.read_csv("data/dataset.csv", index_col=0)
# datetime_series = pd.to_datetime(
#     df[['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE']])
# df['DATA'] = datetime_series
# df.dropna(subset=['NEIGHBOURHOOD'], inplace=True)


# def estacao_do_ano(data):
#     import datetime
#     month = data.month
#     day = data.day
#     year = data.year

#     if (datetime.date(year, month, day) >= datetime.date(year, 3, 20)) and (datetime.date(year, month, day) < datetime.date(year, 6, 21)):
#         return 'Spring'
#     elif (datetime.date(year, month, day) >= datetime.date(year, 6, 21)) and (datetime.date(year, month, day) < datetime.date(year, 9, 23)):
#         return 'Summer'
#     elif (datetime.date(year, month, day) >= datetime.date(year, 9, 23)) and (datetime.date(year, month, day) < datetime.date(year, 12, 21)):
#         return 'Autumn'
#     else:
#         return 'Winter'


# # Aplicar a função para criar uma nova coluna 'estacao'
# df['SEASON'] = df['DATA'].apply(estacao_do_ano)


# # To dict - para salvar no dcc.store
# df_store = df.to_dict()
# figure = None


def CARD(title, id, sm=6, lg=4, md=4, config=config_graph, style=tab_card):
    layout = dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6(title),
                    dcc.Graph(id=id, config=config)], sm=sm, md=md, lg=lg),
            ])
        ])
    ], style=style)
    return layout


def make_tooltip(text, target):
    return dbc.Tooltip(
        text,
        target=target,
    )


layout = dbc.Container(children=[
    # Armazenamento de dataset
    dcc.Store(id='dataset', data=df_store),
    # dcc.Store(id='dataset-fixed', data=df_store),
    dcc.Store(id='controller', data={'play': False}),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.Div(["Choose de month",],
                                 style={"font-size": "80%"}),
                        dcc.Dropdown(
                            id="drop-month-1",
                            value=4,
                            options=[{'label': key, 'value': value}
                                     for key, value in zip(months.keys(), months.values())],
                            clearable=False
                        ),
                    ])
                ], lg=3),
                dbc.Col([
                    html.Div([
                        html.Div(["Choose the year"], style={
                                 "font-size": "80%"}),
                        dcc.Dropdown(
                            id="drop-year-1",
                            value=2020,
                            options=[{'label': i, 'value': i}
                                     for i in df.YEAR.unique()],
                            clearable=False
                        ),
                    ])

                ], lg=3),
                dbc.Col([
                    html.Div([
                        html.Div(["Choose the crime"],
                                 style={'font-size': '80%'}),
                        dcc.Dropdown(
                            id="drop-crime-1",
                            value="Other Theft",
                            options=[{'label': i, "value": i}
                                     for i in df.TYPE.unique()],
                            clearable=False
                        )
                    ])

                ], lg=6),
            ], className='g-2 my-auto', style={'margin-top': '9px'}),
            dbc.Row([
                dbc.Col([
                    CARD("Amount of crimes by month and type",
                         "id-card-indicator-2", lg=12),
                    make_tooltip(
                        "Comparison with previous year by type of crime", "id-card-indicator-2")
                ], lg=3),
                dbc.Col([
                    CARD("Amount of crimes by year and type",
                         "id-card-indicator-1", lg=12),
                    make_tooltip("Comparison with previous year",
                                 "id-card-indicator-1")
                ], lg=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        html.H6("Crime by neighbourhood and type", style={
                                                "display": "inline-block"}),
                                        dbc.Button("More Info", id="open", n_clicks=0, className="btn btn-secondary btn-sm",
                                                   style={"display": "inline-block", "margin-left": "5%"}),
                                        dbc.Modal(
                                            [
                                                dbc.ModalHeader(
                                                    dbc.ModalTitle("Other Neighbourhoods")),
                                                dbc.ModalBody(
                                                    html.Div(
                                                        [
                                                            html.P(id="body"),
                                                            dcc.Graph(
                                                                id="id-graph-modal"),
                                                        ]),
                                                ),
                                                dbc.Button(
                                                    "Close", id="close", className="ms-auto", n_clicks=0)
                                            ],
                                            id="modal",
                                            is_open=False,
                                            size="xl"),
                                    ]),
                                    dcc.Graph(id="id-graph-1", config=config_graph, figure=fig_bar)], lg=12),
                            ])
                        ])
                    ], style=tab_card),
                    dbc.Tooltip(
                        """Distribution of crimes by neighbourhood in a year. The category 'Others 
                        Neighbourhoods means all other neighbourhoods were grouped'""",
                        target="id-graph-1",
                        is_open=False,
                        placement='top'
                    )
                ], lg=6)
            ], className='g-2 my-auto'),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dcc.Dropdown(
                            id="drop-crime-3",
                            multi=True,
                            value=["Theft from Vehicle"],
                            options=[{'label': i, "value": i}
                                     for i in df.TYPE.unique()],
                        ),
                    ], className='g-2 my-auto'),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H6("Crimes Over Year"),
                                            dcc.Graph(id="id-graph-line-1", config=config_graph, figure=fig_multilinhas)], lg=12),
                                    ])
                                ])
                            ], style=tab_card),
                            # CARD("Crimes Over Year", "id-graph-line-1", lg=12),
                            make_tooltip(
                                "Seeing the crimes over year", "id-graph-line-1")
                        ]),
                    ], className='g-2 my-auto'),
                ], lg=6),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(
                                id="drop-bairro-1",
                                value="Fairview",
                                options=[{'label': i, "value": i}
                                         for i in df.NEIGHBOURHOOD.unique()],
                            )
                        ], lg=6),
                        dbc.Col([
                            dcc.Dropdown(
                                id="drop-bairro-2",
                                value="Strathcona",
                                options=[{'label': i, "value": i}
                                         for i in df.NEIGHBOURHOOD.unique()],
                            )
                        ], lg=6)
                    ], className='g-2 my-auto'),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H6("Direct Comparison"),
                                            dcc.Graph(id="id-graph-comparison", config=config_graph)], lg=12),
                                    ])
                                ])
                            ], style=tab_card),
                            # CARD("Direct Comparisson",
                            #      "id-graph-comparison", lg=12),
                            html.P(id='desc_comparison', style={
                                   'color': 'gray', 'font-size': '80%'}),
                        ], lg=12)
                    ], className='g-2 my-auto',)
                ], lg=6)
            ], className='g-2 my-auto'),
            dbc.Row([
                dbc.Col(
                    [
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        html.H6("Analysis by season"),
                                        dcc.Graph(id="id-estacao-graph", config=config_graph, figure=fig_estacoes)], lg=12),
                                ])
                            ])
                        ], style=tab_card),
                        # CARD("Análise por estações", "id-estacao-graph", lg=12),
                    ], lg=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                    dbc.Col([
                                        html.H6("Analysis by period of day"),
                                        dcc.Graph(id="id-periodo", config=config_graph, figure=fig_periodo)], lg=12),
                                    ])
                        ])
                    ], style=tab_card),

                    # CARD("Análise por período", "id-periodo", lg=12)
                ], lg=6)
            ], className='g-2 my-auto')

        ], className='g-2 my-auto'),])


], fluid=True)


# ====================== CARD indicador 1
@app.callback(
    Output('id-card-indicator-2', 'figure'),
    [Input('dataset', 'data'),
     Input('drop-month-1', 'value'),
     Input('drop-crime-1', 'value'),
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
@cache.memoize(timeout=10)  # in seconds
def update_graph(data, month, crime_selected, toggle):
    # template = template_theme1 if toggle else template_theme2
    df = pd.DataFrame(data)
    year = 2022
    datetime_series = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE']].rename(
        columns={'YEAR': 'YEAR', 'MONTH': 'MONTH', 'DAY': 'DAY', 'HOUR': 'HOUR', 'MINUTE': 'MINUTE'}))
    df.loc[:, 'DATE'] = datetime_series
    df_crimes = df.groupby([pd.PeriodIndex(df['DATE'], freq="M"), 'YEAR', 'MONTH', 'TYPE'])[
        'HUNDRED_BLOCK'].count().reset_index().rename(columns={'HUNDRED_BLOCK': 'COUNTING'})
    dff = df_crimes[(df_crimes.YEAR.isin([year])) & (
        (df_crimes.MONTH.isin([month])) | (df_crimes.MONTH.isin([month-1])))]
    # Limpando as variáveis"
    del df

    dff = dff.drop(['YEAR', 'MONTH'], axis=1)
    for crime in df_crimes.TYPE.unique():
        for date in dff.DATE.unique():
            if dff[(dff['DATE'] == date) & (dff['TYPE'] == crime)].empty:
                dff.loc[dff.index[-1] + 1, :] = [date, crime, 0]
    dff['COUNTING'] = dff['COUNTING'].astype(int)
    df_filtered = dff[dff.TYPE.isin([crime_selected])]

# Limpando as variáveis"
    del dff

    df_filtered = df_filtered.sort_values(['TYPE', 'DATE', 'COUNTING'])
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=df_filtered.at[df_filtered.index[-1], 'COUNTING'],
        number={'valueformat': '.0f', 'font': {'size': 40}},
        title={"text": f"<span style='font-size:1.8em'>{crime_selected}</span><br><span style='font-size:1em'>{year} - {year-1}</span>"},
        delta={'relative': True, 'valueformat': '.1%',
               'reference': df_filtered.at[df_filtered.index[0], 'COUNTING']},
        domain={'x': [0, 1], 'y': [0.05, 0.8]}
    ))
    fig.update_layout(main_config, height=170)
    del df_filtered
    return fig


# ====================== CARD indicador 2
@app.callback(
    Output('id-card-indicator-1', 'figure'),
    [Input('dataset', 'data'),
     Input('drop-year-1', 'value'),
     Input('drop-crime-1', 'value'),
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def update_graph(data, year, crime, toggle):
    template = template_theme1 if toggle else template_theme2
    df = pd.DataFrame(data)
    dff = df[df['TYPE'] == crime]
    aux = dff.groupby(['YEAR']).count()['DAY'].reset_index().rename(
        columns={'DAY': 'COUNTING'})
    fig_indicator = go.Figure()
    fig_indicator.add_trace(go.Indicator(
        mode="number+delta",
        title={"text": f"<span style='font-size:1.8em'>{crime}</span><br><span style='font-size:1em'>{year} - {year-1}</span>"},
        value=aux[aux.YEAR.isin([year])]['COUNTING'].values[0],
        number={'valueformat': '.0f', 'font': {'size': 40}},
        delta={'relative': True, 'valueformat': '.1%',
               'reference': aux[aux.YEAR.isin([year-1])]['COUNTING'].values[0]},
        domain={'x': [0, 1], 'y': [0.05, 0.8]}
    ))
    del aux, dff, df
    fig_indicator.update_layout(main_config, height=170, template=template)
    return fig_indicator


@app.callback(
    [Output('id-graph-1', 'figure'),
     Output('body', 'children'),
     Output('id-graph-modal', 'figure')],
    [Input('drop-year-1', 'value'),
     Input('drop-crime-1', 'value'),]
)
def update_graph(year, crime):
    # template = template_theme1 if toggle else template_theme2

    dff = aux_bar[(aux_bar.TYPE.isin([crime])) & (aux_bar.YEAR.isin([year]))]

    aux = dff.copy()
    dff.loc[:, 'NEIGHBOURHOOD'] = np.where(
        dff.loc[:, "COUNTING"] < dff.at[dff.index[3], "COUNTING"], "Others Neighbourhoods", dff['NEIGHBOURHOOD'])

    dff = dff.groupby(['TYPE', 'YEAR', 'NEIGHBOURHOOD'])['COUNTING'].sum(
    ).reset_index().sort_values(['COUNTING'])

    fig_bar = px.bar(dff, x='COUNTING', y='NEIGHBOURHOOD',
                     title=None, color='COUNTING', color_continuous_scale="fall")
    fig_bar.update_layout(main_config, height=170,
                          yaxis_title=None, xaxis_title=None)

    all_bairros = aux.NEIGHBOURHOOD.unique().tolist()
    grouped_bairros = dff.NEIGHBOURHOOD.unique().tolist()
    others_bairros = list(set(all_bairros).difference(grouped_bairros))

    mask = aux.NEIGHBOURHOOD.isin(others_bairros)
    fig_detail = px.bar(aux[mask].sort_values(['COUNTING']), x='COUNTING', y='NEIGHBOURHOOD',
                        title=None, color='COUNTING', color_continuous_scale="fall")
    fig_detail.update_layout(main_config, height=350,
                             yaxis_title=None, xaxis_title=None)

    text = f"Os bairros são: {others_bairros}"
    # print(text)

    del dff

    return [fig_bar, text, fig_detail]

# # ====================== Grafico de linha


@app.callback(
    Output("id-graph-line-1", 'figure'),
    [Input('drop-crime-3', 'value'),]
)
@cache.memoize(timeout=10)  # in seconds
def update_graph(crimes):
    # template = template_theme1 if toggle else template_theme2
    if crimes is []:
        # Evita a execução do callback se o valor for None
        raise dash.exceptions.PreventUpdate
    else:

        mask = aux_multi.TYPE.isin(crimes)
        fig_multilinhas = px.line(aux_multi[mask], x='YEAR', y='COUNTING',
                                  color='TYPE',
                                  color_discrete_sequence=["#3F5A42", "#818F6E", "#8F9B78", "#B4B890", "#CECDA2", "#F4EBBB",
                                                           "#F3DCAC", "#F1CE9E", "#E7A575", "#E9AB7B", "#E09161"])
        # updates
        fig_multilinhas.update_layout(
            main_config, height=250, xaxis_title=None, yaxis_title=None)

        del mask
        return fig_multilinhas

# # ======================= Grafico comparacao


@app.callback(
    [Output("id-graph-comparison", 'figure'),
     Output('desc_comparison', 'children')],
    [Input('dataset', 'data'),
     Input('drop-crime-1', 'value'),
     Input('drop-bairro-1', 'value'),
     Input('drop-bairro-2', 'value'),
     Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
@cache.memoize(timeout=10)  # in seconds
def update_graph(data, crime, bairro1, bairro2, toggle):

    df1 = df[(df.TYPE.isin([crime])) & (df.NEIGHBOURHOOD.isin([bairro1]))]
    df2 = df[(df.TYPE.isin([crime])) & (df.NEIGHBOURHOOD.isin([bairro2]))]
    df_bairro1 = df1.groupby(pd.PeriodIndex(df1['DATA'], freq="M"))[
        'DAY'].count().reset_index().rename(columns={'DAY': 'COUNTING'})
    df_bairro2 = df2.groupby(pd.PeriodIndex(df2['DATA'], freq="M"))[
        'DAY'].count().reset_index().rename(columns={'DAY': 'COUNTING'})
    df_bairro1['DATA'] = pd.PeriodIndex(df_bairro1['DATA'], freq="M")
    df_bairro2['DATA'] = pd.PeriodIndex(df_bairro2['DATA'], freq="M")
    df_final = pd.DataFrame()
    df_final['DATA'] = df_bairro1['DATA'].astype('datetime64[ns]')
    df_final['COUNTING'] = df_bairro1['COUNTING']-df_bairro2['COUNTING']

    del df1, df2, df_bairro1, df_bairro2

    fig = go.Figure()
    # Toda linha
    fig.add_scattergl(
        name=bairro1, x=df_final['DATA'], y=df_final['COUNTING'], line=dict(color='#3D5941'))
    # Abaixo de zero
    fig.add_scattergl(name=bairro2, x=df_final['DATA'], y=df_final['COUNTING'].where(
        df_final['COUNTING'] > 0.00000), line=dict(color='#CA562C'))
    # Updates
    del df_final
    fig.update_layout(main_config, height=165)
    # fig.update_yaxes(range = [-0.7,0.7])
    # Annotations pra mostrar quem é o mais barato
    fig.add_annotation(text=f'{bairro1} had more crimes',
                       xref="paper", yref="paper",
                       font=dict(
                           family="Courier New, monospace",
                           size=12,
                           color="#ffffff"
                       ),
                       align="center", bgcolor="rgba(0,0,0,0.5)", opacity=0.8,
                       x=0.5, y=0.75, showarrow=False)
    fig.add_annotation(text=f'{bairro2} had more crimes',
                       xref="paper", yref="paper",
                       font=dict(
                           family="Courier New, monospace",
                           size=12,
                           color="#ffffff"
                       ),
                       align="center", bgcolor="rgba(0,0,0,0.5)", opacity=0.8,
                       x=0.5, y=0.25, showarrow=False)
    # Definindo o texto
    text_comparison = f"Comparison between {bairro2} and {bairro1}. If the line is above the x-axis, it indicates that {bairro2} had fewer selected criminal events; otherwise, {bairro1} had the smallest value."
    return [fig, text_comparison]


# #======================= Gráfico Periodo


@app.callback(
    Output("id-periodo", "figure"),
    [Input('drop-crime-1', 'value'),]
    # Input(ThemeSwitchAIO.ids.switch("theme"), "value")]
)
def update_graph(crime):
    # template = template_theme1 if toggle else template_theme2

    aux = df_crimes[df_crimes.TYPE.isin([crime])]
    fig_periodo = px.pie(aux,
                         names='PERIOD', values='COUNTING', color='COUNTING', color_discrete_sequence=['#3D5941', '#CA562C'])

    fig_periodo.update_layout(main_config, height=200)

    return fig_periodo

# #======================= Gráfico estações


@app.callback(
    Output("id-estacao-graph", "figure"),
    [Input('drop-crime-1', 'value'),
     Input('drop-year-1', 'value'),]
)
def update_graph(crime, year):
    dff = df[(df.TYPE.isin([crime])) & (df.YEAR.isin([year]))]

    fig_estacoes = px.bar(dff.groupby('SEASON')['DAY'].count().reset_index().rename(columns={'DAY': 'COUNTING'}),
                          x='SEASON', y='COUNTING', color='COUNTING', color_continuous_scale='fall')

    fig_estacoes.update_layout(
        main_config, height=200, xaxis_title=None, yaxis_title=None)

    return fig_estacoes

# Trocar os nomes das variáveis. Cada variável tem que ter um nome único. Depois da ação do callback, fazer a limpeza delas


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
