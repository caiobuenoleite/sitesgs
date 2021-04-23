import pandas as pd
import datetime as dt

df_obitos = pd.read_excel(r'.\datasets\ÓBITOS COVID 19 -2020 - 2021.xlsx', sheet_name='CONFIRMADOS', header=3)
df_obitos = df_obitos.dropna(subset=['Nº'])
df_obitos = df_obitos.dropna(subset=['SEXO'])

df_obitos['DATA DO ÓBITO'] = pd.to_datetime(df_obitos['DATA DO ÓBITO'],errors='coerce',format='%Y-%m-%d %H:%M:%S')
df_obitos = df_obitos.dropna(subset=['DATA DO ÓBITO'])
df_obitos = df_obitos[df_obitos['DATA DO ÓBITO']<=dt.datetime.today()]
