import pandas as pd
import datetime as dt

df_ocupacao_leitos = pd.read_excel(r'.\datasets\versaofinal_leitosVigilancia_total.xlsx')

df_ocupacao_leitos['Data'] = pd.to_datetime(df_ocupacao_leitos['Data'],errors='coerce',format='%Y-%m-%d %H:%M:%S')
df_ocupacao_leitos = df_ocupacao_leitos.dropna(subset=['Data'])
df_ocupacao_leitos = df_ocupacao_leitos[df_ocupacao_leitos['Data']<=dt.datetime.today()]

df_ocupacao_leitos['Ocupacao'] = pd.to_numeric(df_ocupacao_leitos['Ocupacao'])
