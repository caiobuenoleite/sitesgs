from etl.bairros import df_por_bairros
import dash_table
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
df_por_bairros = df_por_bairros.rename(columns={'bairro_corrigido':'Bairros'})
df_por_bairros.reset_index(drop=False,inplace=True)


x = df_por_bairros

tabela_bairros = dash_table.DataTable(
    id='table_bairros',
    columns=[{"name": i, "id": i} for i in x.columns],
    data=x.to_dict('records'),
    style_cell={
        'textAlign': 'center',
        'backgroundColor': "#151a28",
        'whiteSpace': 'normal',
        'height': 'auto',
        'width': '{}%'.format(len(x.columns)),
        # 'padding': '5px'
        },
    style_as_list_view=True,
    sort_action='native',
    sort_mode='multi',
    sort_by=[],
    page_current=0,
    page_size=14,
    page_action='native',
    style_data_conditional=[
        { 'if': { 'state': 'active' }, 'backgroundColor': '#808080', 'border': '1px solid #FFFFFF' },
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': '#000'
            },
        {
            'if': {'column_id': 'Óbitos'},
            'color': '#fc2c20'
            },
        {
            'if': {'column_id': 'Confirmados'},
            'color': '#ffa339'
            },
        {
            'if': {'column_id': 'BAIRRO'},
            'color': '#eae0d5'
            }

        ],
    style_header=
        {
            'backgroundColor': "#000",
            'fontWeight': 'bold',
        },
    style_header_conditional=[
        { 'if': {'column_id': 'BAIRRO'},
            'color': '#eae0d5',
            },
        {
            'if': {'column_id': 'Óbitos'},
            'color': '#fc2c20',
            },
        {
            'if': {'column_id': 'Confirmados'},
            'color': '#ffa339'
            }
        ]
)
