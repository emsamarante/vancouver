from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go

from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from graphs import *
import time


app = Dash(__name__)


def CARD(title, id, sm=6, lg=4, md=4, config=config_graph, style=tab_card):
    layout = dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H5(title),
                    dcc.Graph(id=id, config=config, figure=fig)], sm=sm, md=md, lg=lg),
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
                        html.H1("OPTIMIZED"),
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




@app.callback(
    [Output("id-graph-line-1", 'figure'),
     Output("output", 'children')],
    [Input('drop-crime-3', 'value'),]
)
def update_graph(crimes):
    start_time = time.time()
    mask = df.TYPE.isin(crimes)
    fig = px.line(df[mask], x='YEAR', y='COUNTING',
                  color='TYPE')
    # updates
    fig.update_layout(main_config, height=230, xaxis_title=None)
    end_time = time.time()
    tempo = end_time - start_time
    texto = f"It took {round(tempo, 4)} seconds."
    return [fig, texto]


if __name__ == "__main__":
    app.run(debug=True)
