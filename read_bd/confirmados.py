import pandas as pd
import datetime as dt

df_confirmados = pd.read_excel(r'.\datasets\CONFIRMADOS COVID 19 - 2020 - 2021.xlsx', sheet_name='CONFIRMADOS', header=4)
df_confirmados = df_confirmados.dropna(subset=['Nº'])

df_confirmados['NOTIFICAÇÃO'] = pd.to_datetime(df_confirmados['NOTIFICAÇÃO'],errors='coerce',format='%Y-%m-%d %H:%M:%S')
df_confirmados = df_confirmados.dropna(subset=['NOTIFICAÇÃO'])
df_confirmados[df_confirmados['NOTIFICAÇÃO']<=dt.datetime.today()]
df_confirmados = df_confirmados[df_confirmados['NOTIFICAÇÃO']>"2020-02-01"]

df_confirmados_legenda = df_confirmados[['Nº','LEGENDA']]
df_confirmados_legenda.LEGENDA = df_confirmados_legenda.LEGENDA.astype(str)
df_confirmados_legenda = df_confirmados_legenda[df_confirmados_legenda['LEGENDA']!='1900-01-15 00:00:00']
df_confirmados_legenda.LEGENDA = df_confirmados_legenda.LEGENDA.str.replace(',','.')

teste = df_confirmados_legenda.LEGENDA.str.split('.',expand=True)
teste = pd.get_dummies(teste,prefix_sep='|')
nomes_teste = teste.columns.tolist()
nomes_teste =teste.columns.str.split('|').str[1].tolist()
teste.columns = teste.columns.str.split('|').str[1].tolist()
df_confirmados_legenda = df_confirmados_legenda.join(
     teste
)
df_confirmados_legenda = df_confirmados_legenda.groupby(df_confirmados_legenda.columns,axis=1).sum()
df_confirmados_legenda = df_confirmados_legenda[df_confirmados_legenda.columns.drop(list(df_confirmados_legenda.filter(regex='nan')))]

legenda_json = {
    '1':'ÓBITOS  ILPIS',
    '2':'AGUARDANDO BASE DO ESTADO',
    '3':'AGUARDANDO NOTIFICAÇÃO',
    '4':'AGUARDANDO SIVEP',
    '5':'ÓBITO PUÉRPERA',
    '6':'AGUARDANDO D.O',
    '7':'PRESÍDIO',
    '8':'ÓBITO EM RESIDÊNCIA',
    '9':'ÓBITO INFANTIL',
    '10':'PROFISSIONAIS DA SAÚDE',
    '11':'UNIDADE PARTICULAR',
    '12':'CONFIRMADO APÓS CLINICO/IMAGEM',
    '13':'FORA DE ÁREA',
    '14':'HOSPITALIZADO',
    '15':'CURADO',
    '16':'ÓBITO'
}
for key in legenda_json:
    for col in df_confirmados_legenda.columns:
        if col == key:
            df_confirmados_legenda.rename(columns = {col: legenda_json[key]}, inplace=True)
