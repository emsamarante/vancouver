# import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
# import dash_bootstrap_templates
# import pandas as pd
# import layouts
from app import *
# from dash_bootstrap_templates import ThemeSwitchAIO
from pages import analysis,  home, map
import sidebar

# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@1.0.4/dbc.min.css"


app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dcc.Location(id="url"),
            sidebar.layout
        ], sm=4, lg=1),

        dbc.Col([
            html.Div(id="page-content")
        ], sm=8, lg=11,)
    ], style={"margin-top": "7px"}, className='g2 my-auto')
], fluid=True, style={'height': '100%'})


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    # if pathname == "/":
    #     return home.layout

    if pathname == "/":
        return analysis.layout

    # if pathname == "/map":
    #     return map.layout

    # if pathname == "/analysis":
    #     return analysis.layout


if __name__ == '__main__':
    app.run_server(debug=True)
