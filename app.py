import dash
import dash_bootstrap_components as dbc

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.15.4/css/all.css"]

app = dash.Dash(__name__, external_stylesheets=[FONT_AWESOME, dbc.themes.COSMO], suppress_callback_exceptions = True)

app.scripts.config.serve_locally = True
server = app.server
