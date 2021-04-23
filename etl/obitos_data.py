from read_bd.obitos import df_obitos
import pandas as pd
import datetime as dt

obitos_por_data = df_obitos.groupby(['DATA DO ÓBITO'])['DATA DO ÓBITO'].count()
obitos_por_data = pd.DataFrame(obitos_por_data)
obitos_por_data = obitos_por_data.rename(columns={'DATA DO ÓBITO':'Casos obitos'})
obitos_por_data.reset_index(drop=False,inplace=True)

valordiario_obitos = obitos_por_data.tail(1)['Casos obitos']
valordiario_obitos = valordiario_obitos.values[0]

datadiaria_obitos = obitos_por_data.tail(1)['DATA DO ÓBITO']
datadiaria_obitos = datadiaria_obitos.dt.strftime('%d/%m/%Y')
datadiaria_obitos = datadiaria_obitos.values[0]
