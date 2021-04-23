from read_bd.ocupacao import df_ocupacao_leitos
import pandas as pd

df_ocupacao_leitos_uti = df_ocupacao_leitos[df_ocupacao_leitos['Tipo de Leito']=='UTI']
df_ocupacao_leitos_uti = df_ocupacao_leitos_uti[['Data', 'Ocupacao']]
df_ocupacao_leitos_uti = df_ocupacao_leitos_uti.groupby(['Data'])['Ocupacao'].mean()
df_ocupacao_leitos_uti = pd.DataFrame(df_ocupacao_leitos_uti)
df_ocupacao_leitos_uti.reset_index(drop=False,inplace=True)
df_ocupacao_leitos_uti.rename(columns={'Ocupacao':'UTI / CTI'},inplace=True)
df_ocupacao_leitos_enf = df_ocupacao_leitos[df_ocupacao_leitos['Tipo de Leito']=='Enfermaria']
df_ocupacao_leitos_enf = df_ocupacao_leitos_enf[['Data', 'Ocupacao']]
df_ocupacao_leitos_enf = df_ocupacao_leitos_enf.groupby(['Data'])['Ocupacao'].mean()
df_ocupacao_leitos_enf = pd.DataFrame(df_ocupacao_leitos_enf)
df_ocupacao_leitos_enf.reset_index(drop=False,inplace=True)
df_ocupacao_leitos_enf.rename(columns={'Ocupacao':'Enfermaria'},inplace=True)

df_ocupacao_leitos_final = pd.merge(df_ocupacao_leitos_uti,df_ocupacao_leitos_enf,how='inner',on='Data')
df_ocupacao_leitos_final[['UTI / CTI']] = df_ocupacao_leitos_final[['UTI / CTI']]
df_ocupacao_leitos_final[['Enfermaria']] = df_ocupacao_leitos_final[['Enfermaria']]
