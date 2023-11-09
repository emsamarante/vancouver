from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from graphs import *
from dash_bootstrap_templates import load_figure_template
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

load_figure_template("cyborg")


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
                    CARD("Amount of Crimes by Month and Type",
                         "id-card-indicator-2", lg=12),
                    make_tooltip(
                        "Comparison with previous year by type of crime", "id-card-indicator-2")
                ], lg=3),
                dbc.Col([
                    CARD("Amount of Crimes by Year and Type",
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
                                        html.H6("Crime by Neighbourhood and Type", style={
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
                                                                id="id-graph-modal", style={"margin": "4%"}),
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
                                         for i in sorted(df.NEIGHBOURHOOD.unique())],
                            )
                        ], lg=6),
                        dbc.Col([
                            dcc.Dropdown(
                                id="drop-bairro-2",
                                value="Strathcona",
                                options=[{'label': i, "value": i}
                                         for i in sorted(df.NEIGHBOURHOOD.unique())],
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
                            ], style={'height': '81%'}),
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
                                        html.H6("Analysis by Season"),
                                        dcc.Graph(id="id-estacao-graph", config=config_graph, figure=fig_estacoes)], lg=12),
                                ])
                            ])
                        ], style=tab_card),
                    ], lg=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                    dbc.Col([
                                        html.H6("Analysis by Period of Day"),
                                        dcc.Graph(id="id-periodo", config=config_graph, figure=fig_periodo)], lg=12),
                                    ])
                        ])
                    ], style=tab_card),
                ], lg=6)
            ], className='g-2 my-auto', style={'margin-bottom': '2%'})

        ], className='g-2 my-auto'),])


], fluid=True)


# Amount of crimes by month and type =====
@app.callback(
    Output('id-card-indicator-2', 'figure'),
    [Input('dataset', 'data'),
     Input('drop-month-1', 'value'),
     Input('drop-crime-1', 'value')]
)
@cache.memoize(timeout=TIMEOUT)  # in seconds
def update_graph(data, month, crime_selected):

    df = pd.DataFrame(data)
    year = 2022

    datetime_series = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']].rename(
        columns={'YEAR': 'YEAR', 'MONTH': 'MONTH', 'DAY': 'DAY'}))

    df.loc[:, 'DATE'] = datetime_series
    df_crimes = df.groupby([pd.PeriodIndex(df['DATE'], freq="M"), 'YEAR', 'MONTH', 'TYPE'])[
        'Counts'].sum().reset_index()
    dff = df_crimes[(df_crimes.YEAR.isin([year])) & (
        (df_crimes.MONTH.isin([month])) | (df_crimes.MONTH.isin([month-1])))]

    del df

    dff = dff.drop(['YEAR', 'MONTH'], axis=1)
    for crime in df_crimes.TYPE.unique():
        for date in dff.DATE.unique():
            if dff[(dff['DATE'] == date) & (dff['TYPE'] == crime)].empty:
                dff.loc[dff.index[-1] + 1, :] = [date, crime, 0]
    dff['Counts'] = dff['Counts'].astype(int)
    df_filtered = dff[dff.TYPE.isin([crime_selected])]

    del dff

    df_filtered = df_filtered.sort_values(['TYPE', 'DATE', 'Counts'])
    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=df_filtered.at[df_filtered.index[-1], 'Counts'],
        number={'valueformat': '.0f', 'font': {'size': 40}},
        title={"text": f"<span style='font-size:1.8em'>{crime_selected}</span><br><span style='font-size:1em'>{year} - {year-1}</span>"},
        delta={'relative': True, 'valueformat': '.1%',
               'reference': df_filtered.at[df_filtered.index[0], 'Counts'],
               'increasing': {'color': red}, 'decreasing': {'color': green}},
        domain={'x': [0, 1], 'y': [0.05, 0.8]}
    ))
    fig.update_layout(main_config, height=140, template=template)
    del df_filtered
    return fig


# Amount of crimes by year and type ===
@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output('id-card-indicator-1', 'figure'),
    [Input('dataset', 'data'),
     Input('drop-year-1', 'value'),
     Input('drop-crime-1', 'value')]
)
def update_graph(data, year, crime):
    df = pd.DataFrame(data)
    dff = df[df['TYPE'] == crime]
    aux = dff.groupby(['YEAR']).sum()['Counts'].reset_index()

    fig_indicator = go.Figure()
    fig_indicator.add_trace(go.Indicator(
        mode="number+delta",
        title={"text": f"<span style='font-size:1.8em'>{crime}</span><br><span style='font-size:1em'>{year} - {year-1}</span>"},
        value=aux[aux.YEAR.isin([year])]['Counts'].values[0],
        number={'valueformat': '.0f', 'font': {'size': 40}},
        delta={'relative': True, 'valueformat': '.1%',
               'reference': aux[aux.YEAR.isin([year-1])]['Counts'].values[0],
               'increasing': {'color': red}, 'decreasing': {'color': green}},
        domain={'x': [0, 1], 'y': [0.05, 0.8]}
    ))
    del aux, dff, df
    fig_indicator.update_layout(main_config, height=140, template=template)
    return fig_indicator

# Crime by neighbourhood and type ===


@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    [Output('id-graph-1', 'figure'),
     Output('body', 'children'),
     Output('id-graph-modal', 'figure')],
    [Input('drop-year-1', 'value'),
     Input('drop-crime-1', 'value')],
    prevent_initial_call=False
)
def update_graph(year, crime):
    dff = aux_bar[(aux_bar.TYPE.isin([crime])) & (aux_bar.YEAR.isin([year]))]

    aux = dff.copy()
    average = dff.groupby(['TYPE', 'YEAR'])['Counts'].mean(
    ).reset_index().sort_values(['Counts'])

    average_value = average.loc[0, 'Counts']

    dff.loc[:, 'NEIGHBOURHOOD'] = np.where(
        dff.loc[:, "Counts"] < dff.at[dff.index[3], "Counts"], "Others Neighbourhoods", dff['NEIGHBOURHOOD'])

    dff = dff.groupby(['TYPE', 'YEAR', 'NEIGHBOURHOOD'])['Counts'].sum(
    ).reset_index().sort_values(['Counts'])

    fig_bar = px.bar(dff, x='Counts', y='NEIGHBOURHOOD',
                     title=None, color='Counts',
                     color_continuous_scale=colorscale_res)

    fig_bar.add_vline(x=average_value, line_width=3,
                      line_dash="dash", line_color="white", label=dict(text=None))
    fig_bar.update_layout(main_config, height=140,
                          yaxis_title=None, xaxis_title=None, template=template)
    fig_bar.add_annotation(text=f"Average: {round(average_value,1)}",
                           xref="paper", yref="paper",
                           font=dict(
                               family="Courier New, monospace",
                               size=12,
                               color="#ffffff"
                           ),
                           align="center", bgcolor="rgba(0,0,0,0.5)", opacity=0.8,
                           x=0.15, y=0.1, showarrow=False)

    all_bairros = aux.NEIGHBOURHOOD.unique().tolist()
    grouped_bairros = dff.NEIGHBOURHOOD.unique().tolist()
    others_bairros = list(set(all_bairros).difference(grouped_bairros))

    mask = aux.NEIGHBOURHOOD.isin(others_bairros)

    # Fig in modal element
    fig_detail = px.bar(aux[mask].sort_values(['Counts']), x='Counts', y='NEIGHBOURHOOD',
                        title=None, color='Counts', color_continuous_scale=colorscale_res)
    fig_detail.update_layout(main_config, height=350,
                             yaxis_title=None, xaxis_title=None)
    fig_detail.add_vline(x=average_value, line_width=3,
                         line_dash="dash", line_color="white", label=dict(text=None))

    fig_detail.add_annotation(text=f"Average: {round(average_value,1)}",
                              xref="paper", yref="paper",
                              font=dict(
                                  family="Courier New, monospace",
                                  size=12,
                                  color="#ffffff"
                              ),
                              align="center", bgcolor="rgba(0,0,0,0.5)", opacity=0.8,
                              x=0.6, y=0.1, showarrow=False)
    text = f"Os bairros são: {others_bairros}"
    text = None

    del dff

    return [fig_bar, text, fig_detail]

# Crimes Over Year ===


@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output("id-graph-line-1", 'figure'),
    [Input('drop-crime-3', 'value'),]
)
def update_graph(crimes):
    if crimes is []:
        # Avoid crash
        raise dash.exceptions.PreventUpdate
    else:

        mask = aux_multi.TYPE.isin(crimes)
        fig_multilinhas = px.line(aux_multi[mask], x='YEAR', y='Counts',
                                  color='TYPE',
                                  )
        # updates
        fig_multilinhas.update_layout(
            main_config, height=215, xaxis_title=None, yaxis_title=None)

        del mask
        return fig_multilinhas

# Direct Comparison ==


@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    [Output("id-graph-comparison", 'figure'),
     Output('desc_comparison', 'children')],
    [Input('drop-crime-1', 'value'),
     Input('drop-bairro-1', 'value'),
     Input('drop-bairro-2', 'value')]
)
def update_graph(crime, bairro1, bairro2):

    datetime_series = pd.to_datetime(
        df[['YEAR', 'MONTH', 'DAY']])
    df.loc[:, 'DATA'] = datetime_series

    df1 = df[(df.TYPE.isin([crime])) & (df.NEIGHBOURHOOD.isin([bairro1]))]
    df2 = df[(df.TYPE.isin([crime])) & (df.NEIGHBOURHOOD.isin([bairro2]))]

    df_bairro1 = df1.groupby(pd.PeriodIndex(df1['DATA'], freq="M"))[
        'Counts'].sum().reset_index()
    df_bairro2 = df2.groupby(pd.PeriodIndex(df2['DATA'], freq="M"))[
        'Counts'].sum().reset_index()
    df_bairro1['DATA'] = pd.PeriodIndex(df_bairro1['DATA'], freq="M")
    df_bairro2['DATA'] = pd.PeriodIndex(df_bairro2['DATA'], freq="M")
    df_final = pd.DataFrame()
    df_final['DATA'] = df_bairro1['DATA'].astype('datetime64[ns]')
    df_final['Counts'] = df_bairro1['Counts']-df_bairro2['Counts']

    del df1, df2, df_bairro1, df_bairro2

    fig = go.Figure()
    # The entire line
    fig.add_scattergl(
        name=bairro1, x=df_final['DATA'], y=df_final['Counts'],)
    line = dict(color='#3D5941')
    # below of zero
    fig.add_scattergl(name=bairro2, x=df_final['DATA'], y=df_final['Counts'].where(
        df_final['Counts'] > 0.00000), )
    line = dict(color='#CA562C')
    # Updates
    del df_final
    fig.update_layout(main_config, height=175)

    # Annotations to show which is safer
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
    text_comparison = f"Comparison between {bairro2} and {bairro1}. If the line is above the x-axis, it indicates that {bairro2} had fewer selected criminal events; otherwise, {bairro1} had the smallest value."
    return [fig, text_comparison]


# Analysis by season ===

@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output("id-estacao-graph", "figure"),
    [Input('drop-crime-1', 'value'),
     Input('drop-year-1', 'value'),]
)
def update_graph(crime, year):
    dff = df[(df.TYPE.isin([crime])) & (df.YEAR.isin([year]))]

    fig_estacoes = px.bar(dff.groupby('SEASON')['PERIOD'].count().reset_index().rename(columns={'PERIOD': 'Counts'}),
                          x='SEASON', y='Counts', color='Counts', color_continuous_scale=colorscale_res)
    fig_estacoes.update_layout(
        main_config, height=170, xaxis_title=None, yaxis_title=None, template=template)
    return fig_estacoes


# Analysis by period of day ===

@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output("id-periodo", "figure"),
    [Input('drop-crime-1', 'value'),]
)
def update_graph(crime):
    aux = df_crimes[df_crimes.TYPE.isin([crime])]
    fig_periodo = px.pie(aux,
                         names='PERIOD', values='Counts', color='Counts', template=template)
    fig_periodo.update_layout(main_config, height=170)

    return fig_periodo

# Modal element ===


@cache.memoize(timeout=TIMEOUT)  # in seconds
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
