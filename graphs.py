import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import numpy as np
load_figure_template("cyborg")


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

red = "#CC0000"
orange = "#FF8E17"
green = "#80B912"
blue = "#2A9FD6"

colorscale_res = [
    (0, blue),   # Cor para valores mínimos
    (1, red),    # Cor para valores máximos
]
colorscale = [
    (0, blue),   # Cor para valores mínimos
    (0.33, green),
    (0.66, orange),
    (1, red),    # Cor para valores máximos
]


template_theme1 = "cyborg"
template_theme2 = "cyborg"
url_theme1 = dbc.themes.CYBORG
url_theme2 = dbc.themes.CYBORG
template = 'cyborg'

# ================================ data
df0 = pd.read_csv("data/dataset_agg.csv", index_col=0)
# datetime_series = pd.to_datetime(
#     df0[['YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE']])
# df0['DATA'] = datetime_series

# del datetime_series
# df0.dropna(subset=['NEIGHBOURHOOD'], inplace=True)


# def estacao_do_ano(data):
#     import datetime
#     month = data.month
#     day = data.day
#     year = data.year

#     if (datetime.date(year, month, day) >= datetime.date(year, 3, 20)) and (datetime.date(year, month, day) < datetime.date(year, 6, 21)):
#         return 'Spring'
#     elif (datetime.date(year, month, day) >= datetime.date(year, 6, 21)) and (datetime.date(year, month, day) < datetime.date(year, 9, 23)):
#         return 'Summer'
#     elif (datetime.date(year, month, day) >= datetime.date(year, 9, 23)) and (datetime.date(year, month, day) < datetime.date(year, 12, 21)):
#         return 'Autumn'
#     else:
#         return 'Winter'


# # Aplicar a função para criar uma nova coluna 'estacao'
# df0['SEASON'] = df0['DATA'].apply(estacao_do_ano)

# To dict - para salvar no dcc.store
df_store = df0.to_dict()
df = pd.DataFrame(df_store)

# print(df.columns)

# Criando gráfico de barra ===========================================
aux_bar = df.groupby(['TYPE', 'YEAR', 'NEIGHBOURHOOD']).sum()[
    'COUNTING'].reset_index()

aux_bar = aux_bar.sort_values(['COUNTING', 'NEIGHBOURHOOD'],
                              ascending=False).reset_index()


fig_bar = px.bar(aux_bar, x='COUNTING', y='NEIGHBOURHOOD',
                 title=None, template=template)
fig_bar.update_layout(main_config, height=170,
                      yaxis_title=None, template=template)

# Gráfico multilinhas =================================================
df = pd.DataFrame(df_store)
aux_multi = df.groupby(['TYPE', 'YEAR'])['PERIOD'].count(
).reset_index().rename(columns={'PERIOD': 'COUNTING'})

fig_multilinhas = px.line(aux_multi, x='YEAR', y='COUNTING',
                          color='TYPE')
fig_multilinhas.update_layout(
    main_config, height=230, xaxis_title=None, template=template)


# Criando gráfico comparison ==========================================
#
#
#

# Criando gráfico estacoes ==========================================
df = pd.DataFrame(df_store)
fig_estacoes = px.bar(df.groupby('SEASON')['COUNTING'].sum().reset_index(),
                      x='SEASON', y='COUNTING')

fig_estacoes.update_layout(main_config, height=200,
                           xaxis_title=None, template=template)

# Criando gráfico período ===========================================
df = pd.DataFrame(df_store)
# df.loc[:, 'PERIOD'] = None
# df.loc[:, 'PERIOD'] = np.where(df.loc[:, 'HOUR'] <= 11, 'AM', 'PM')
# df_crimes = df.groupby(['PERIOD', 'TYPE'])['DAY'].count(
# ).reset_index().rename(columns={'DAY': 'COUNTING'})
df_crimes = df.groupby(['PERIOD', 'TYPE'])['COUNTING'].sum(
).reset_index()


fig_periodo = px.pie(df_crimes,
                     names='PERIOD', values='COUNTING', color='COUNTING', template=template)

fig_periodo.update_layout(main_config, height=200)
