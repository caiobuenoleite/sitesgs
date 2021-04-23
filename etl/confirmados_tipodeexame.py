from read_bd.confirmados import df_confirmados
import pandas as pd

df_confirmados['CONF. LABORATORIAL OU VINCULO'] = df_confirmados['CONF. LABORATORIAL OU VINCULO'].str.upper()
df_confirmados['CONF. LABORATORIAL OU VINCULO'] = df_confirmados['CONF. LABORATORIAL OU VINCULO'].str.strip()
df_confirmados['CONF. LABORATORIAL OU VINCULO'] = df_confirmados['CONF. LABORATORIAL OU VINCULO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df_confirmados['CONF. LABORATORIAL OU VINCULO'].replace('PCR+ BASE',"PCR", inplace=True)
df_confirmados['CONF. LABORATORIAL OU VINCULO'].replace('RT-PCR',"PCR", inplace=True)
df_confirmados['CONF. LABORATORIAL OU VINCULO'].replace('PCR+BASE SIVEP',"PCR", inplace=True)
df_confirmados['CONF. LABORATORIAL OU VINCULO'].replace('IGN',"IGNORADO", inplace=True)
df_confirmados['CONF. LABORATORIAL OU VINCULO'].replace('TR + IGM',"TESTE RAPIDO", inplace=True)
df_confirmados['CONF. LABORATORIAL OU VINCULO'].replace('TR POSITIVO+ BASE SIVEP',"TESTE RAPIDO", inplace=True)
df_confirmados['CONF. LABORATORIAL OU VINCULO'].replace('SOROLOGIA PARA COVID-19, ANTICORPOS TOTAIS (IGM / IGG)',"SOROLOGIA", inplace=True)
df_confirmados['CONF. LABORATORIAL OU VINCULO'].replace('ANTI-COVID-19, ANTICORPOS IGGQ',"SOROLOGIA", inplace=True)
df_confirmados['CONF. LABORATORIAL OU VINCULO'].replace('ANTI-COVID-19, ANTICORPOS IGMQ',"SOROLOGIA", inplace=True)
df_confirmados['CONF. LABORATORIAL OU VINCULO'].replace('ANTI-SARS-COV-2, ANTICORPOS NEUTRALIZANTES',"SOROLOGIA", inplace=True)
confirmados_por_tipo_teste = df_confirmados.groupby(['CONF. LABORATORIAL OU VINCULO'])['CONF. LABORATORIAL OU VINCULO'].count()
confirmados_por_tipo_teste = pd.DataFrame(confirmados_por_tipo_teste)
confirmados_por_tipo_teste = confirmados_por_tipo_teste.rename(columns={'CONF. LABORATORIAL OU VINCULO':'Casos Confirmados'})
confirmados_por_tipo_teste.reset_index(drop=False,inplace=True)

