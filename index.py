from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from app import *
from pages import analysis,  home, maps


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem(
                    "Analysis", href="/analysis", id='id-load-trigger'),
                dbc.DropdownMenuItem("Maps", href="/maps"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Criminal Events Analysis",
    brand_href="#",
    color="danger",
    dark=True,
)

app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dcc.Location(id="url"),
            navbar
        ], sm=4, lg=12),], style={"margin-top": "7px"}, className='g2 my-auto'),
    dbc.Row([
        dbc.Col([
            html.Div(id="page-content")
        ], sm=8, lg=12,)
    ], style={"margin-top": "7px"}, className='g2 my-auto')
], fluid=True, style={'height': '100%'})


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return home.layout

    elif pathname == "/maps":
        return maps.layout

    elif pathname == "/analysis":
        return analysis.layout


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
