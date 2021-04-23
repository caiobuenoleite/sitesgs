from etl.bairros import df_por_bairros
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

lista_bairros = pd.read_excel(r'.\datasets\lista_bairros.xlsx')

lista_bairros.SINAN = lista_bairros.SINAN.str.upper()
lista_bairros.SINAN = lista_bairros.SINAN.str.strip()
lista_bairros.SINAN = lista_bairros['SINAN'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

lista_bairros.sort_values(by='SINAN',inplace=True)
df_por_bairros.sort_values(by='BAIRRO',inplace=True)


bairro_corrigido = []
similarity = []
for i in df_por_bairros.BAIRRO:
        ratio = process.extract( i, lista_bairros.SINAN, limit=1)
        bairro_corrigido.append(ratio[0][0])
        similarity.append(ratio[0][1])
df_por_bairros['bairro_corrigido'] = pd.Series(bairro_corrigido)
df_por_bairros['similarity'] = pd.Series(similarity)
df_por_bairros = df_por_bairros[df_por_bairros.similarity>=85]

df_por_bairros = df_por_bairros.groupby(['bairro_corrigido'])['Confirmados' ,'Óbitos'].sum()
df_por_bairros = pd.DataFrame(df_por_bairros)
df_por_bairros.rename(columns={'bairro_corrigido':'Bairros'},inplace=True)
df_por_bairros.reset_index(drop=False,inplace=True)


print(df_por_bairros.columns)
