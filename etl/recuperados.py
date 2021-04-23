from read_bd.confirmados import df_confirmados_legenda, df_confirmados
import datetime as dt
from datetime import timedelta
import pandas as pd

df_recuperados = df_confirmados_legenda.copy()

lista_obitos = list(df_recuperados.filter(regex='ÓBITO'))

for l in lista_obitos:
    for col in df_recuperados.columns:
        if l == col:
            df_recuperados = df_recuperados[(df_recuperados[[col]] != 1).any(axis=1)]

df_recuperados.loc[:,'Curado'] = "Não"

df_recuperados = df_recuperados.merge(df_confirmados, on='Nº',how='left')
df_recuperados =df_recuperados.drop(columns='LEGENDA_y')
df_recuperados = df_recuperados.rename(columns={
    'LEGENDA_x':'LEGENDA'
})
df_recuperados = df_recuperados[df_recuperados['NOTIFICAÇÃO']<=dt.datetime.today()]
df_recuperados.loc[:,'Data_Cura'] = df_recuperados['NOTIFICAÇÃO'] + timedelta(days=21)
df_recuperados.loc[df_recuperados['CURADO'] == 1,"Curado"] = "Sim"
df_recuperados.loc[df_recuperados['CURADO'] == 1,"Data_Cura"] = df_recuperados.loc[df_recuperados['CURADO'] == 1,"NOTIFICAÇÃO"]
df_recuperados.loc[df_recuperados['Data_Cura']<=max(df_recuperados['NOTIFICAÇÃO']),"Curado"] = "Sim"
df_recuperados = df_recuperados[df_recuperados["Curado"]=="Sim"]
df_recuperados = df_recuperados.sort_values(by=['Data_Cura'], ascending=True)

recuperados_por_data = df_recuperados.groupby(['Data_Cura'])['Data_Cura'].count()
recuperados_por_data = pd.DataFrame(recuperados_por_data)
recuperados_por_data = recuperados_por_data.rename(columns={'Data_Cura':'Casos recuperados'})
recuperados_por_data.reset_index(drop=False,inplace=True)

valordiario_recuperados = recuperados_por_data.tail(1)['Casos recuperados']
valordiario_recuperados = valordiario_recuperados.values[0]

datadiaria_recuperados = recuperados_por_data.tail(1)['Data_Cura']
datadiaria_recuperados = datadiaria_recuperados.dt.strftime('%d/%m/%Y')
datadiaria_recuperados = datadiaria_recuperados.values[0]

print(valordiario_recuperados)
