from read_bd.confirmados import df_confirmados
import pandas as pd
import datetime as dt

confirmados_por_data = df_confirmados[df_confirmados['NOTIFICAÇÃO']<=dt.datetime.today()]

confirmados_por_data = confirmados_por_data.groupby(['NOTIFICAÇÃO'])['NOTIFICAÇÃO'].count()
confirmados_por_data = pd.DataFrame(confirmados_por_data)
confirmados_por_data = confirmados_por_data.rename(columns={'NOTIFICAÇÃO':'Casos Confirmados'})
confirmados_por_data.reset_index(drop=False,inplace=True)

valordiario_confirmados = confirmados_por_data.tail(1)['Casos Confirmados']
valordiario_confirmados = valordiario_confirmados.values[0]

datadiaria_confirmados = confirmados_por_data.tail(1)['NOTIFICAÇÃO']
datadiaria_confirmados = datadiaria_confirmados.dt.strftime('%d/%m/%Y')
datadiaria_confirmados = datadiaria_confirmados.values[0]
