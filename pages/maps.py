from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


df_map = pd.read_csv("data/dataset.csv", index_col=0)
df_store_map = df_map.to_dict()

layout = dbc.Container(children=[
    # Armazenamento de dataset
    dcc.Store(id='dataset', data=df_store_map),
    # dcc.Store(id='dataset-fixed', data=df_store),
    dbc.Row([
        html.H1("Dash map")
    ])
])
