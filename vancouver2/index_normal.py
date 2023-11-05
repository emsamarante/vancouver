from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go

from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from graphs import *
import pandas as pd
import time


config_graph = {"displayModeBar": False, "showTips": False}
tab_card = {'height': '100%'}
main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor": "top",
               "y": 0.9,
               "xanchor": "left",
               "x": 0.1,
               "title": {"text": None},
               "font": {"color": "white"},
               "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l": 0, "r": 0, "t": 10, "b": 0}
}
months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, ' June': 6, 'July': 7, 'August': 8, 'September': 9,
          'October': 10, 'November': 11, 'December': 12}

# ================================ data
df = pd.read_csv("dataset.csv", index_col=0)
datetime_series = pd.to_datetime(
    df[['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE']])
df['DATA'] = datetime_series
df.dropna(subset=['NEIGHBOURHOOD'], inplace=True)


def estacao_do_ano(data):
    import datetime
    month = data.month
    day = data.day
    year = data.year

    if (datetime.date(year, month, day) >= datetime.date(year, 3, 20)) and (datetime.date(year, month, day) < datetime.date(year, 6, 21)):
        return 'Spring'
    elif (datetime.date(year, month, day) >= datetime.date(year, 6, 21)) and (datetime.date(year, month, day) < datetime.date(year, 9, 23)):
        return 'Summer'
    elif (datetime.date(year, month, day) >= datetime.date(year, 9, 23)) and (datetime.date(year, month, day) < datetime.date(year, 12, 21)):
        return 'Autumn'
    else:
        return 'Winter'


# Aplicar a função para criar uma nova coluna 'estacao'
df['SEASON'] = df['DATA'].apply(estacao_do_ano)


# To dict - para salvar no dcc.store
df_store = df.to_dict()


def CARD(title, id, sm=6, lg=4, md=4, config=config_graph, style=tab_card):
    layout = dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H5(title),
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


app = Dash(__name__)


def CARD(title, id, sm=6, lg=4, md=4, config=config_graph, style=tab_card):
    layout = dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H5(title),
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


app.layout = dbc.Container(children=[
    # Armazenamento de dataset
    dcc.Store(id='dataset', data=df_store),
    # dcc.Store(id='dataset-fixed', data=df_store),
    # dcc.Store(id='controller', data={'play': False}),
    dbc.Row([
        dbc.Col([
            dbc.Col([
                    dbc.Row([
                        html.H1("ORDINARY"),
                        html.Div(id='output'),
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
                            CARD("Crimes Over Year", "id-graph-line-1", lg=12),
                        ]),
                    ], className='g-2 my-auto'),
                    ], lg=6),
        ], className='g-2 my-auto'),])
], fluid=True)


# ====================== CARD indicador 1


@app.callback(
    [Output("id-graph-line-1", 'figure'),
     Output("output", 'children')],
    [Input('dataset', 'data'),
     Input('drop-crime-3', 'value'),]
)
def update_graph(data, crimes):
    start = time.time()
    df = pd.DataFrame(data)

    if crimes is []:
        # Evita a execução do callback se o valor for None
        raise dash.exceptions.PreventUpdate
    else:
        df = df.groupby(['TYPE', 'YEAR'])['DAY'].count(
        ).reset_index().rename(columns={'DAY': 'COUNTING'})
        mask = df.TYPE.isin(crimes)
        fig = px.line(df[mask], x='YEAR', y='COUNTING',
                      color='TYPE')
        # updates
        fig.update_layout(main_config, height=230, xaxis_title=None)
        end = time.time()
        tempo = end - start
        texto = f"It took {round(tempo, 4)} seconds."
        return [fig, texto]


if __name__ == "__main__":
    app.run(debug=True, port=8051)
