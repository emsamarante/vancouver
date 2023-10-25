from dash import html
import dash_bootstrap_components as dbc
# from dash_bootstrap_templates import ThemeSwitchAIO


tab_card = {'height': '98vh', 'margin-top': '1vh', "align-items": "center",
            "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 50px 0 rgba(0, 0, 0, 0.3)"}

template_theme1 = "cyborg"
template_theme2 = "cyborg"
url_theme1 = dbc.themes.CYBORG
url_theme2 = dbc.themes.CYBORG

# Icons
ico_home = html.I(className="fa fa-city",
                  style={'font-size': '250%', 'margin-top': '5vh', 'margin-left': '20px'})
ico_map = html.I(className="fas fa-map-marked",
                 style={'font-size': '250%', 'margin-top': '5vh', 'margin-left': '20px'})
ico_chart = html.I(className="fas fa-chart-bar",
                   style={'font-size': '250%', 'margin-top': '5vh', 'margin-left': '20px'})

# Nav
nav = dbc.Nav([
    dbc.NavLink(ico_home, href="/", active="exact"),
    dbc.NavLink(ico_map, href="/map", active="exact"),
    dbc.NavLink(ico_chart, href="/analysis", active="exact")
])


layout = dbc.Card(
    [
        dbc.Row([], style={'margin-top': '5vh'}),
        # ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
        nav
    ], style=tab_card
)
