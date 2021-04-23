from read_bd.confirmados import df_confirmados
from read_bd.obitos import df_obitos
import pandas as pd

df_confirmados.BAIRRO = df_confirmados.BAIRRO.str.upper()
df_confirmados.BAIRRO = df_confirmados.BAIRRO.str.strip()
df_confirmados.BAIRRO = df_confirmados['BAIRRO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

confirmados_por_genero = df_confirmados.groupby(['BAIRRO'])['BAIRRO'].count()
confirmados_por_genero = pd.DataFrame(confirmados_por_genero)
confirmados_por_genero = confirmados_por_genero.rename(columns={'BAIRRO':'Confirmados'})
confirmados_por_genero.reset_index(drop=False,inplace=True)

df_obitos.BAIRRO = df_obitos.BAIRRO.str.upper()
df_obitos.BAIRRO = df_obitos.BAIRRO.str.strip()
df_obitos.BAIRRO = df_obitos['BAIRRO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

confirmados_por_genero2 = df_obitos.groupby(['BAIRRO'])['BAIRRO'].count()
confirmados_por_genero2 = pd.DataFrame(confirmados_por_genero2)
confirmados_por_genero2 = confirmados_por_genero2.rename(columns={'BAIRRO':'Óbitos'})
confirmados_por_genero2.reset_index(drop=False,inplace=True)

df_por_bairros = pd.merge(confirmados_por_genero,confirmados_por_genero2, on="BAIRRO")

