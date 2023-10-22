import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np


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


template_theme1 = "cosmo"
template_theme2 = "solar"
url_theme1 = dbc.themes.COSMO
url_theme2 = dbc.themes.SOLAR

# ================================ data
df = pd.read_csv("data/dataset.csv", index_col=0)
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
df = pd.DataFrame(df_store)


# Criando gráfico de barra ===========================================
aux = df.groupby(['TYPE', 'YEAR', 'NEIGHBOURHOOD']).count()[
    'DAY'].reset_index().rename(columns={'DAY': 'COUNTING'})

aux = aux.sort_values(['COUNTING', 'NEIGHBOURHOOD'],
                      ascending=False).reset_index()


fig_bar = px.bar(aux, x='COUNTING', y='NEIGHBOURHOOD', title=None)
fig_bar.update_layout(main_config, height=170,
                      yaxis_title=None)

# Gráfico multilinhas =================================================
df = pd.DataFrame(df_store)
aux_multi = df.groupby(['TYPE', 'YEAR'])['DAY'].count(
).reset_index().rename(columns={'DAY': 'COUNTING'})

fig_multilinhas = px.line(aux_multi, x='YEAR', y='COUNTING',
                          color='TYPE')
fig_multilinhas.update_layout(main_config, height=230, xaxis_title=None)


# Criando gráfico comparison ==========================================
df = pd.DataFrame(df_store)
crime = "Other Theft"
year = 2020
bairro1 = "Fairview"
bairro2 = "Strathcona"

df1 = df[(df.TYPE.isin([crime])) & (df.NEIGHBOURHOOD.isin([bairro1]))]
df2 = df[(df.TYPE.isin([crime])) & (df.NEIGHBOURHOOD.isin([bairro2]))]
df_bairro1 = df1.groupby(pd.PeriodIndex(df1['DATA'], freq="M"))[
    'DAY'].count().reset_index().rename(columns={'DAY': 'COUNTING'})
df_bairro2 = df2.groupby(pd.PeriodIndex(df2['DATA'], freq="M"))[
    'DAY'].count().reset_index().rename(columns={'DAY': 'COUNTING'})
df_bairro1['DATA'] = pd.PeriodIndex(df_bairro1['DATA'], freq="M")
df_bairro2['DATA'] = pd.PeriodIndex(df_bairro2['DATA'], freq="M")
df_final = pd.DataFrame()
df_final['DATA'] = df_bairro1['DATA'].astype('datetime64[ns]')
df_final['COUNTING'] = df_bairro1['COUNTING']-df_bairro2['COUNTING']

del df_bairro1

fig_comparison = go.Figure()
# Toda linha
fig_comparison.add_scattergl(
    name=bairro1, x=df_final['DATA'], y=df_final['COUNTING'])
# Abaixo de zero
fig_comparison.add_scattergl(name=bairro2, x=df_final['DATA'], y=df_final['COUNTING'].where(
    df_final['COUNTING'] > 0.00000))
# Updates
fig_comparison.update_layout(main_config, height=180)
# fig.update_yaxes(range = [-0.7,0.7])
# Annotations pra mostrar quem é o mais barato
fig_comparison.add_annotation(text=f'{bairro2} mais barato',
                              xref="paper", yref="paper",
                              font=dict(
                                  family="Courier New, monospace",
                                  size=12,
                                  color="#ffffff"
                              ),
                              align="center", bgcolor="rgba(0,0,0,0.5)", opacity=0.8,
                              x=0.5, y=0.75, showarrow=False)
fig_comparison.add_annotation(text=f'{bairro2} mais barato',
                              xref="paper", yref="paper",
                              font=dict(
                                  family="Courier New, monospace",
                                  size=12,
                                  color="#ffffff"
                              ),
                              align="center", bgcolor="rgba(0,0,0,0.5)", opacity=0.8,
                              x=0.5, y=0.25, showarrow=False)
# Definindo o texto
text_comparison = f"Comparando {bairro2} e {bairro1}. Se a linha estiver acima do eixo X, {bairro2} tinha menor preço, do contrário, {bairro1} tinha um valor inferior"
