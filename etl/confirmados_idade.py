from read_bd.confirmados import df_confirmados
import pandas as pd
import numpy as np

df_confirmados.IDADE.replace('1M',0, inplace=True)
df_confirmados.IDADE.replace('1 M',0, inplace=True)
df_confirmados.IDADE.replace('2M',0, inplace=True)
df_confirmados.IDADE.replace('2 M',0, inplace=True)
df_confirmados.IDADE.replace('3M',0, inplace=True)
df_confirmados.IDADE.replace('3 M',0, inplace=True)
df_confirmados.IDADE.replace('4M',0, inplace=True)
df_confirmados.IDADE.replace('4 M',0, inplace=True)
df_confirmados.IDADE.replace('5M',0, inplace=True)
df_confirmados.IDADE.replace('5 M',0, inplace=True)
df_confirmados.IDADE.replace('6M',0, inplace=True)
df_confirmados.IDADE.replace('6 M',0, inplace=True)
df_confirmados.IDADE.replace('7M',0, inplace=True)
df_confirmados.IDADE.replace('7 M',0, inplace=True)
df_confirmados.IDADE.replace('8M',0, inplace=True)
df_confirmados.IDADE.replace('8 M',0, inplace=True)
df_confirmados.IDADE.replace('9M',0, inplace=True)
df_confirmados.IDADE.replace('1 MES',0, inplace=True)
df_confirmados.IDADE.replace('1 MÊS',0, inplace=True)
df_confirmados.IDADE.replace('2 MESES',0, inplace=True)
df_confirmados.IDADE.replace('3 MESES',0, inplace=True)
df_confirmados.IDADE.replace('4 MESES',0, inplace=True)
df_confirmados.IDADE.replace('5 MESES',0, inplace=True)
df_confirmados.IDADE.replace('6 MESES',0, inplace=True)
df_confirmados.IDADE.replace('7 MESES',0, inplace=True)
df_confirmados.IDADE.replace('8 MESES',0, inplace=True)
df_confirmados.IDADE.replace('9 MESES',0, inplace=True)

df_confirmados['IDADE'].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')
df_confirmados['IDADE'] = pd.to_numeric(df_confirmados['IDADE'],errors='coerce',downcast='signed')
df_confirmados = df_confirmados[df_confirmados.IDADE>=0]
df_confirmados.IDADE = df_confirmados.IDADE.astype("int")

bins = [0, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99, np.inf]
names = ['De 0 à 9 anos', 'De 10 à 19 anos', 'De 20 à 29 anos', 'De 30 à 39 anos', 'De 40 à 49 anos','De 50 à 59 anos', 'De 60 à 69 anos', 'De 70 à 79 anos', 'De 80 à 89 anos','De 90 à 99 anos', 'Maior de 100']

df_confirmados['Faixa Etária'] = pd.cut(df_confirmados['IDADE'], bins, labels=names)
confirmados_por_idade = df_confirmados.groupby(['Faixa Etária'])['Faixa Etária'].count()
confirmados_por_idade = pd.DataFrame(confirmados_por_idade)
confirmados_por_idade = confirmados_por_idade.rename(columns={'Faixa Etária':'Casos Confirmados'})
confirmados_por_idade.reset_index(drop=False,inplace=True)
