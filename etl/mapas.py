from read_bd.confirmados import df_confirmados
from read_bd.obitos import df_obitos
from etl.geolocate import df_bairros_bases_final
import pandas as pd

df_confirmados.BAIRRO = df_confirmados.BAIRRO.str.upper()
df_confirmados.BAIRRO = df_confirmados.BAIRRO.str.strip()
df_confirmados.BAIRRO = df_confirmados['BAIRRO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_bairros_confirmados = df_confirmados.groupby(['BAIRRO'])['BAIRRO'].count()
df_bairros_confirmados = pd.DataFrame(df_bairros_confirmados)
df_bairros_confirmados = df_bairros_confirmados.rename(columns={'BAIRRO':'Variável'})
df_bairros_confirmados.reset_index(drop=False,inplace=True)
df_bairros_bases_final2 = df_bairros_bases_final[['BAIRRO', 'lat', 'lon']]
df_bairros_confirmados_com_geo = pd.merge(df_bairros_confirmados,df_bairros_bases_final2, how='left',on='BAIRRO')

df_obitos.BAIRRO = df_obitos.BAIRRO.str.upper()
df_obitos.BAIRRO = df_obitos.BAIRRO.str.strip()
df_obitos.BAIRRO = df_obitos['BAIRRO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_bairros_obitos = pd.DataFrame(df_obitos.BAIRRO)
df_bairros_obitos = df_obitos.groupby(['BAIRRO'])['BAIRRO'].count()
df_bairros_obitos = pd.DataFrame(df_bairros_obitos)
df_bairros_obitos = df_bairros_obitos.rename(columns={'BAIRRO':'Variável'})
df_bairros_obitos.reset_index(drop=False,inplace=True)
df_bairros_obitos_com_geo = pd.merge(df_bairros_obitos,df_bairros_bases_final, how='left',on='BAIRRO')

# df_por_bairros = pd.merge(confirmados_por_genero,confirmados_por_genero2, on="BAIRRO")

