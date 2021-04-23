from read_bd.confirmados import df_confirmados
from read_bd.obitos import df_obitos
from geopy.geocoders import GoogleV3
import pandas as pd

df_confirmados.BAIRRO = df_confirmados.BAIRRO.str.upper()
df_confirmados.BAIRRO = df_confirmados.BAIRRO.str.strip()
df_confirmados.BAIRRO = df_confirmados['BAIRRO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_bairros_confirmados = pd.DataFrame(df_confirmados.BAIRRO.unique())

df_obitos.BAIRRO = df_obitos.BAIRRO.str.upper()
df_obitos.BAIRRO = df_obitos.BAIRRO.str.strip()
df_obitos.BAIRRO = df_obitos['BAIRRO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_bairros_obitos = pd.DataFrame(df_obitos.BAIRRO.unique())

df_bairros_bases = df_bairros_confirmados.append(df_bairros_obitos)
df_bairros_bases.rename(columns={0:'BAIRRO'},inplace=True)
df_bairros_bases = pd.DataFrame(df_bairros_bases.BAIRRO.unique())
df_bairros_bases.rename(columns={0:'BAIRRO'},inplace=True)
# df_bairros_bases = df_bairros_bases.BAIRRO.tolist()
df_bairros_bases_final = df_bairros_bases
df_bairros_bases_final['lat'] = 0.0000000
df_bairros_bases_final['lon'] = 0.0000000
AUTH_KEY = "AIzaSyA-dulzoEbkNMZnor6jAO3UnWDJz4cSjNQ"
geolocator = GoogleV3(api_key=AUTH_KEY)

list_bairros = {}

for i in range(0,df_bairros_bases.shape[0]):
    data = geolocator.geocode("Bairro: " + df_bairros_bases.BAIRRO[i] + " São Gonçalo - RJ").point
    df_bairros_bases_final.lat[i] = data[0]
    df_bairros_bases_final.lon[i] = data[1]
    # list_bairros.update({''f"{df_bairros_bases[i]}":''f"{data}"})

# confirmados_por_genero2 = df_obitos.groupby(['BAIRRO'])['BAIRRO'].count()
# confirmados_por_genero2 = pd.DataFrame(confirmados_por_genero2)
# confirmados_por_genero2 = confirmados_por_genero2.rename(columns={'BAIRRO':'Óbitos'})
# confirmados_por_genero2.reset_index(drop=False,inplace=True)

# df_por_bairros = pd.merge(confirmados_por_genero,confirmados_por_genero2, on="BAIRRO")
df_bairros_bases_final.to_excel('./datasets/geoDB.xlsx')

