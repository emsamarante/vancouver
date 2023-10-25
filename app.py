import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache
from dash_bootstrap_templates import load_figure_template
import os

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.15.4/css/all.css"]

load_figure_template("journal")
app = dash.Dash(__name__, external_stylesheets=[
                FONT_AWESOME, dbc.themes.JOURNAL])

cache = Cache(app.server, config={
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', '')
})
app.config.suppress_callback_exceptions = True


app.scripts.config.serve_locally = True
server = app.server
