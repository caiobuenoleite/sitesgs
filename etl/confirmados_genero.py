from read_bd.confirmados import df_confirmados
import pandas as pd

df_confirmados.SEXO = df_confirmados.SEXO.str.upper()
df_confirmados.SEXO = df_confirmados.SEXO.str.strip()
df_confirmados.SEXO.replace('F',"Feminino", inplace=True)
df_confirmados.SEXO.replace('M',"Masculino", inplace=True)
confirmados_por_genero = df_confirmados.groupby(['SEXO'])['SEXO'].count()
confirmados_por_genero = pd.DataFrame(confirmados_por_genero)
confirmados_por_genero = confirmados_por_genero.rename(columns={'SEXO':'Casos Confirmados'})
confirmados_por_genero.reset_index(drop=False,inplace=True)

