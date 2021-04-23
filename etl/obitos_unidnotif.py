from os import replace
from read_bd.obitos import df_obitos
import pandas as pd

df_obitos['UNIDADE DE REFERÊNCIA '] = df_obitos['UNIDADE DE REFERÊNCIA '].str.upper()
df_obitos['UNIDADE DE REFERÊNCIA '] = df_obitos['UNIDADE DE REFERÊNCIA '].str.strip()
df_obitos['UNIDADE DE REFERÊNCIA '] = df_obitos['UNIDADE DE REFERÊNCIA '].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_obitos['UNIDADE DE REFERÊNCIA '].replace('ANTI-SARS-COV-2, ANTICORPOS NEUTRALIZANTES',"SOROLOGIA", inplace=True)
df_obitos['UNIDADE DE REFERÊNCIA '].replace("ESTADUAL F.A","ESTADUAL FA",inplace=True)
df_obitos['UNIDADE DE REFERÊNCIA '].replace("FEDERAL F.A","FEDERAL FA",inplace=True)
df_obitos['UNIDADE DE REFERÊNCIA '].replace("MUNICIPAL F.A","MUNICIPAL FA",inplace=True)
df_obitos['UNIDADE DE REFERÊNCIA '].replace("PRIVADO F.A","PRIVADO FA",inplace=True)
df_obitos['UNIDADE DE REFERÊNCIA '].replace("HEAT","ESTADUAL",inplace=True)
obitos_unidade_notificadora = df_obitos.groupby(['UNIDADE DE REFERÊNCIA '])['UNIDADE DE REFERÊNCIA '].count()
obitos_unidade_notificadora = pd.DataFrame(obitos_unidade_notificadora)
obitos_unidade_notificadora = obitos_unidade_notificadora.rename(columns={'UNIDADE DE REFERÊNCIA ':'Obitos Confirmados'})
obitos_unidade_notificadora.reset_index(drop=False,inplace=True)
