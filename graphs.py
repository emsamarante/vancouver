import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
load_figure_template("cyborg")


# Utils

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
months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
          ' June': 6, 'July': 7, 'August': 8, 'September': 9,
          'October': 10, 'November': 11, 'December': 12}

red = "#CC0000"
orange = "#FF8E17"
green = "#80B912"
blue = "#2A9FD6"

colorscale_res = [
    (0, blue),   # Cor para valores mínimos
    (1, red),    # Cor para valores máximos
]


template = 'cyborg'


#############################################################################
#
#   Screen - Analysis
#
#############################################################################


# ================================ data
df0 = pd.read_csv("data/dataset_agg.csv", index_col=0)


# To dict - para salvar no dcc.store
df_store = df0.to_dict()
df = pd.DataFrame(df_store)


# Criando gráfico de barra ===========================================
aux_bar = df.groupby(['TYPE', 'YEAR', 'NEIGHBOURHOOD']).sum()[
    'Counts'].reset_index()

aux_bar = aux_bar.sort_values(['Counts', 'NEIGHBOURHOOD'],
                              ascending=False).reset_index()


fig_bar = px.bar(aux_bar, x='Counts', y='NEIGHBOURHOOD',
                 title=None, template=template)
fig_bar.update_layout(main_config, height=170,
                      yaxis_title=None, template=template)

# Gráfico multilinhas =================================================
df = pd.DataFrame(df_store)
aux_multi = df.groupby(['TYPE', 'YEAR'])['PERIOD'].count(
).reset_index().rename(columns={'PERIOD': 'Counts'})

fig_multilinhas = px.line(aux_multi, x='YEAR', y='Counts',
                          color='TYPE')
fig_multilinhas.update_layout(
    main_config, height=230, xaxis_title=None, template=template)


# Criando gráfico estacoes ==========================================
df = pd.DataFrame(df_store)
fig_estacoes = px.bar(df.groupby('SEASON')['Counts'].sum().reset_index(),
                      x='SEASON', y='Counts')

fig_estacoes.update_layout(main_config, height=200,
                           xaxis_title=None, template=template)

# Criando gráfico período ===========================================
df = pd.DataFrame(df_store)
df_crimes = df.groupby(['PERIOD', 'TYPE'])['Counts'].sum(
).reset_index()
fig_periodo = px.pie(df_crimes,
                     names='PERIOD', values='Counts', color='Counts',
                     template=template)
fig_periodo.update_layout(main_config, height=200)


#############################################################################
#
#   Screen - Maps
#
#############################################################################

df_map0 = pd.read_csv("data/dataset_mapa.csv", index_col=0)
df_store_map = df_map0.sample(1000).to_dict()
df_map = pd.DataFrame(df_store_map)


# Maps
df_map = pd.DataFrame(df_store_map)
fig_map = px.scatter_mapbox(
    df_map, lat="Lat", lon="Long", hover_name="TYPE",
    color='MONTH', zoom=11, height=710)
fig_map.update_layout(mapbox_style="carto-darkmatter")
fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


# relative bar
df_map = pd.DataFrame(df_store_map)

initial = ['Arbutus Ridge', 'Central Business District',
           'Dunbar-Southlands', 'Fairview', 'Grandview-Woodland',
           'Hastings-Sunrise']


mask = df_map.NEIGHBOURHOOD.isin(initial)

fig_bar_season = px.histogram(df_map[mask].sort_values(['NEIGHBOURHOOD', "SEASON"]),
                              x="NEIGHBOURHOOD",
                              color="SEASON",
                              barnorm="percent",
                              text_auto=True,
                              color_discrete_sequence=[
                                  "#80B912", "#333333", "#626262", "#A0A2A1"],
                              )
fig_bar_season.update_layout(main_config, height=330, yaxis_title="Percent", xaxis_title=None
                             )
# fig_bar_season.update_xaxes(categoryorder='total descending')
fig_bar_season.update_traces(
    textfont_size=12, textangle=0, cliponaxis=True, texttemplate='%{y:.0f}')

# absolute bar
df_map = pd.DataFrame(df_store_map)

initial = ['Arbutus Ridge', 'Central Business District',
           'Dunbar-Southlands', 'Fairview', 'Grandview-Woodland',
           'Hastings-Sunrise']


mask = df_map.NEIGHBOURHOOD.isin(initial)

fig_bar_season_abs = px.bar(df_map[mask].groupby(['SEASON', 'NEIGHBOURHOOD'])['Lat'].size(
).reset_index().rename(columns={"Lat": "Counts"}),
    x='NEIGHBOURHOOD', y='Counts', color='SEASON',
    color_discrete_sequence=[
    "#80B912", "#333333", "#626262", "#A0A2A1"],
)

fig_bar_season_abs.update_layout(main_config, height=330, yaxis_title="Percent", xaxis_title=None
                                 )
# fig_bar_season_abs.update_xaxes(categoryorder='total descending')
fig_bar_season_abs.update_traces(
    textfont_size=12, textangle=0, cliponaxis=True, texttemplate='%{y:.0f}')
