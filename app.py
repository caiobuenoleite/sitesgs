'''
Cabeçalho:

 ESTADO DO RIO DE JANEIRO
 PREFEITURA MUNICIPAL DE SÃO GONÇALO
 SECRETARIA MUNICIPAL DE SAÚDE E DEFESA CIVIL
 SUPERINTENDÊNCIA DE SAÚDE COLETIVA
 DEPARTAMENTO DE EPIDEMIOLOGIA E CONTROLE DE AGRAVOS
 DIVISÃO DE VIGILÂNCIA EPIDEMIOLÓGICA
 COORDENADORA: GLÁUCIA DE OLIVEIRA PINHEIRO CAPIBARIBE

'''
# -*- coding: utf-8 -*-

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import datetime as dt
from templates.navbar import navbar
from templates.cards_diarios import card1
from templates.card_graficos import card3
from templates.card_intermediario import card2
from dash.dependencies import Input, Output, State
from plots.confirmados_genero import fig_confirmados_genero
from plots.confirmados_idade import fig_confirmados_idade
from plots.mapas import mapa_obitos,mapa_confirmados
from plots.obitos import fig_obitos_data
from plots.ocupacao import fig_ocupacao
from etl.confirmados_data import confirmados_por_data
from etl.obitos_data import obitos_por_data
from etl.ocupacao import df_ocupacao_leitos_final
from read_bd.obitos import df_obitos
from etl.geolocate import df_bairros_bases_final
from read_bd.confirmados import df_confirmados
import pandas as pd
import numpy as np
import plotly.express as px
import dash_table
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd

external_stylesheets = ['./assets/site.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    navbar,
    card1,
    card2,
    card3
])

#########################  Categoricos

@app.callback(
    Output('fig_grafico_conf_genero','figure'),
    [Input('id_radioitens','value'),
    Input(component_id='filtro_datas', component_property='start_date'),
    Input(component_id='filtro_datas', component_property='end_date')]
)
def selecao(valor,start_date, end_date):
    if valor=="id_genero_radiobtn":
        temp = df_confirmados[(df_confirmados['NOTIFICAÇÃO']>=start_date) & (df_confirmados['NOTIFICAÇÃO'] <=end_date)]
        temp.SEXO = temp.SEXO.str.upper()
        temp.SEXO = temp.SEXO.str.strip()
        temp.SEXO.replace('F',"Feminino", inplace=True)
        temp.SEXO.replace('M',"Masculino", inplace=True)
        confirmados_por_genero = temp.groupby(['SEXO'])['SEXO'].count()
        confirmados_por_genero = pd.DataFrame(confirmados_por_genero)
        confirmados_por_genero = confirmados_por_genero.rename(columns={'SEXO':'Casos Confirmados'})
        confirmados_por_genero.reset_index(drop=False,inplace=True)
        fig_confirmados_genero = px.bar(
            confirmados_por_genero,
            x='Casos Confirmados',
            y='SEXO',
            orientation='h',
            labels={
                'Casos Confirmados':'Casos Confirmados',
                'SEXO':'Gênero'
            },
        )
        fig_confirmados_genero.update_traces(hovertemplate=(
                        'Casos Confirmados: %{x}'+
                        '<br>Gênero: %{y}<extra></extra>'
                    ))
        fig_confirmados_genero.update_layout(xaxis_tickformat = '###.###.###')
        layout = fig_confirmados_genero.update_layout(
            paper_bgcolor='#151a28',
            plot_bgcolor='#151a28'
        )
        fig_confirmados_genero.update_layout(
            font_family="Courier New Bold",
            font_color="#e4e8f1",
            font_size=16,
            title_font_family="Times New Roman",
            title_font_color="#e4e8f1",
            legend_title_font_color="#e4e8f1"
        )
        fig_confirmados_genero.update_xaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_confirmados_genero.update_yaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_confirmados_genero.update_xaxes(title_font_family="Arial Bold")
        fig_confirmados_genero.update_layout(title_text='Casos confirmados por Gênero')#,height=350,width=780)
        fig_confirmados_genero.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
        fig_confirmados_genero.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6)
        return fig_confirmados_genero
    if valor=="id_tipotestagem_radiobtn":
        temp = df_confirmados[(df_confirmados['NOTIFICAÇÃO']>=start_date) & (df_confirmados['NOTIFICAÇÃO'] <=end_date)]
        temp['CONF. LABORATORIAL OU VINCULO'] = temp['CONF. LABORATORIAL OU VINCULO'].str.upper()
        temp['CONF. LABORATORIAL OU VINCULO'] = temp['CONF. LABORATORIAL OU VINCULO'].str.strip()
        temp['CONF. LABORATORIAL OU VINCULO'] = temp['CONF. LABORATORIAL OU VINCULO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        temp['CONF. LABORATORIAL OU VINCULO'].replace('PCR+ BASE',"PCR", inplace=True)
        temp['CONF. LABORATORIAL OU VINCULO'].replace('RT-PCR',"PCR", inplace=True)
        temp['CONF. LABORATORIAL OU VINCULO'].replace('PCR+BASE SIVEP',"PCR", inplace=True)
        temp['CONF. LABORATORIAL OU VINCULO'].replace('IGN',"IGNORADO", inplace=True)
        temp['CONF. LABORATORIAL OU VINCULO'].replace('TR + IGM',"TESTE RAPIDO", inplace=True)
        temp['CONF. LABORATORIAL OU VINCULO'].replace('TR POSITIVO+ BASE SIVEP',"TESTE RAPIDO", inplace=True)
        temp['CONF. LABORATORIAL OU VINCULO'].replace('SOROLOGIA PARA COVID-19, ANTICORPOS TOTAIS (IGM / IGG)',"SOROLOGIA", inplace=True)
        temp['CONF. LABORATORIAL OU VINCULO'].replace('ANTI-COVID-19, ANTICORPOS IGGQ',"SOROLOGIA", inplace=True)
        temp['CONF. LABORATORIAL OU VINCULO'].replace('ANTI-COVID-19, ANTICORPOS IGMQ',"SOROLOGIA", inplace=True)
        temp['CONF. LABORATORIAL OU VINCULO'].replace('ANTI-SARS-COV-2, ANTICORPOS NEUTRALIZANTES',"SOROLOGIA", inplace=True)
        confirmados_por_tipo_teste = temp.groupby(['CONF. LABORATORIAL OU VINCULO'])['CONF. LABORATORIAL OU VINCULO'].count()
        confirmados_por_tipo_teste = pd.DataFrame(confirmados_por_tipo_teste)
        confirmados_por_tipo_teste = confirmados_por_tipo_teste.rename(columns={'CONF. LABORATORIAL OU VINCULO':'Casos Confirmados'})
        confirmados_por_tipo_teste =confirmados_por_tipo_teste[confirmados_por_tipo_teste['Casos Confirmados']>=140]
        confirmados_por_tipo_teste.reset_index(drop=False,inplace=True)

        fig_confirmados_genero = px.bar(
            confirmados_por_tipo_teste,
            x='Casos Confirmados',
            y='CONF. LABORATORIAL OU VINCULO',
            orientation='h',
            labels={
                'Casos Confirmados':'Casos Confirmados',
                'CONF. LABORATORIAL OU VINCULO':'Tipo de testagem'
            },
        )
        fig_confirmados_genero.update_traces(hovertemplate=(
                        'Casos Confirmados: %{x}'+
                        '<br>Tipo de testagem: %{y}<extra></extra>'
                    ))
        fig_confirmados_genero.update_layout(xaxis_tickformat = '###.###.###')
        layout = fig_confirmados_genero.update_layout(
            paper_bgcolor='#151a28',
            plot_bgcolor='#151a28'
        )
        fig_confirmados_genero.update_layout(
            font_family="Courier New Bold",
            font_color="#e4e8f1",
            font_size=16,
            title_font_family="Times New Roman",
            title_font_color="#e4e8f1",
            legend_title_font_color="#e4e8f1"
        )
        fig_confirmados_genero.update_xaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_confirmados_genero.update_yaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_confirmados_genero.update_xaxes(title_font_family="Arial Bold")
        fig_confirmados_genero.update_layout(title_text='Casos confirmados por Tipo de testagem')#,height=350,width=780)
        fig_confirmados_genero.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
        fig_confirmados_genero.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6)
        return fig_confirmados_genero
    if valor=="id_obtnotif_radiobtn":
        temp = df_obitos[(df_obitos['DATA DO ÓBITO']>=start_date) & (df_obitos['DATA DO ÓBITO'] <=end_date)]
        temp['LOCAL DO ÓBITO'] = temp['LOCAL DO ÓBITO'].str.upper()
        temp['LOCAL DO ÓBITO'] = temp['LOCAL DO ÓBITO'].str.strip()
        temp['LOCAL DO ÓBITO'] = temp['LOCAL DO ÓBITO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        # temp['LOCAL DO ÓBITO'].replace('ANTI-SARS-COV-2, ANTICORPOS NEUTRALIZANTES',"SOROLOGIA", inplace=True)
        # temp['LOCAL DO ÓBITO'].replace("ESTADUAL F.A","ESTADUAL FA",inplace=True)
        # temp['LOCAL DO ÓBITO'].replace("FEDERAL F.A","FEDERAL FA",inplace=True)
        # temp['LOCAL DO ÓBITO'].replace("MUNICIPAL F.A","MUNICIPAL FA",inplace=True)
        # temp['LOCAL DO ÓBITO'].replace("PRIVADA","PRIVADO",inplace=True)
        # temp['LOCAL DO ÓBITO'].replace("PRIVADA F.A","PRIVADO FA",inplace=True)
        # temp['LOCAL DO ÓBITO'].replace("PRIVADO F.A","PRIVADO FA",inplace=True)
        # temp['LOCAL DO ÓBITO'].replace("HEAT","ESTADUAL",inplace=True)
        # temp['LOCAL DO ÓBITO'].replace("PRIVADA FA","PRIVADO FA",inplace=True)
        obitos_unidade_notificadora = temp.groupby(['LOCAL DO ÓBITO'])['LOCAL DO ÓBITO'].count()
        obitos_unidade_notificadora = pd.DataFrame(obitos_unidade_notificadora)
        obitos_unidade_notificadora = obitos_unidade_notificadora.rename(columns={'LOCAL DO ÓBITO':'Obitos Confirmados'})
        obitos_unidade_notificadora.reset_index(drop=False,inplace=True)
        fig_obitos_unidade_notificadora = px.bar(
            obitos_unidade_notificadora,
            x='Obitos Confirmados',
            y='LOCAL DO ÓBITO',
            orientation='h',
            labels={
                'Obitos Confirmados':'Óbitos Confirmados',
                'LOCAL DO ÓBITO':'Unidade de Referência'
            },
        )
        fig_obitos_unidade_notificadora.update_traces(hovertemplate=(
                        'Óbitos Confirmados: %{x}'+
                        '<br>Unidade de Referência: %{y}<extra></extra>'
                    ))
        fig_obitos_unidade_notificadora.update_layout(xaxis_tickformat = '###.###.###')
        layout = fig_obitos_unidade_notificadora.update_layout(
            paper_bgcolor='#151a28',
            plot_bgcolor='#151a28'
        )
        fig_obitos_unidade_notificadora.update_layout(
            font_family="Courier New Bold",
            font_color="#e4e8f1",
            font_size=16,
            title_font_family="Times New Roman",
            title_font_color="#e4e8f1",
            legend_title_font_color="#e4e8f1"
        )
        fig_obitos_unidade_notificadora.update_xaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_obitos_unidade_notificadora.update_yaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_obitos_unidade_notificadora.update_xaxes(title_font_family="Arial Bold")
        fig_obitos_unidade_notificadora.update_layout(title_text='Óbitos confirmados por Unidade Notificadora')#,height=350,width=780)
        fig_obitos_unidade_notificadora.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
        fig_obitos_unidade_notificadora.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6)
        return fig_obitos_unidade_notificadora
    if valor=="id_faixaetaria_radiobtn":
        temp = df_confirmados[(df_confirmados['NOTIFICAÇÃO']>=start_date) & (df_confirmados['NOTIFICAÇÃO'] <=end_date)]
        temp.IDADE.replace('1M',0, inplace=True)
        temp.IDADE.replace('1 M',0, inplace=True)
        temp.IDADE.replace('2M',0, inplace=True)
        temp.IDADE.replace('2 M',0, inplace=True)
        temp.IDADE.replace('3M',0, inplace=True)
        temp.IDADE.replace('3 M',0, inplace=True)
        temp.IDADE.replace('4M',0, inplace=True)
        temp.IDADE.replace('4 M',0, inplace=True)
        temp.IDADE.replace('5M',0, inplace=True)
        temp.IDADE.replace('5 M',0, inplace=True)
        temp.IDADE.replace('6M',0, inplace=True)
        temp.IDADE.replace('6 M',0, inplace=True)
        temp.IDADE.replace('7M',0, inplace=True)
        temp.IDADE.replace('7 M',0, inplace=True)
        temp.IDADE.replace('8M',0, inplace=True)
        temp.IDADE.replace('8 M',0, inplace=True)
        temp.IDADE.replace('9M',0, inplace=True)
        temp.IDADE.replace('1 MES',0, inplace=True)
        temp.IDADE.replace('1 MÊS',0, inplace=True)
        temp.IDADE.replace('2 MESES',0, inplace=True)
        temp.IDADE.replace('3 MESES',0, inplace=True)
        temp.IDADE.replace('4 MESES',0, inplace=True)
        temp.IDADE.replace('5 MESES',0, inplace=True)
        temp.IDADE.replace('6 MESES',0, inplace=True)
        temp.IDADE.replace('7 MESES',0, inplace=True)
        temp.IDADE.replace('8 MESES',0, inplace=True)
        temp.IDADE.replace('9 MESES',0, inplace=True)
        temp['IDADE'].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')
        temp['IDADE'] = pd.to_numeric(temp['IDADE'],errors='coerce',downcast='signed')
        temp = temp[temp.IDADE>=0]
        temp.IDADE = temp.IDADE.astype("int")
        bins = [0, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99, np.inf]
        names = ['De 0 à 9 anos', 'De 10 à 19 anos', 'De 20 à 29 anos', 'De 30 à 39 anos', 'De 40 à 49 anos','De 50 à 59 anos', 'De 60 à 69 anos', 'De 70 à 79 anos', 'De 80 à 89 anos','De 90 à 99 anos', 'Maior de 100']
        temp['Faixa Etária'] = pd.cut(temp['IDADE'], bins, labels=names)
        confirmados_por_idade = temp.groupby(['Faixa Etária'])['Faixa Etária'].count()
        confirmados_por_idade = pd.DataFrame(confirmados_por_idade)
        confirmados_por_idade = confirmados_por_idade.rename(columns={'Faixa Etária':'Casos Confirmados'})
        confirmados_por_idade.reset_index(drop=False,inplace=True)
        fig_confirmados_idade = px.bar(
            confirmados_por_idade,
            x='Casos Confirmados',
            y='Faixa Etária',
            orientation='h',
            labels={
                'Casos Confirmados':'Casos Confirmados',
                'SEXO':'Gênero'
            },
        )
        fig_confirmados_idade.update_traces(hovertemplate=(
                        'Casos Confirmados: %{x}'+
                        '<br>Faixa Etária: %{y}<extra></extra>'
                    ))
        fig_confirmados_idade.update_layout(xaxis_tickformat = '###.###.###')
        layout = fig_confirmados_idade.update_layout(
            paper_bgcolor='#151a28',
            plot_bgcolor='#151a28'
        )
        fig_confirmados_idade.update_layout(
            font_family="Courier New Bold",
            font_color="#e4e8f1",
            font_size=16,
            title_font_family="Times New Roman",
            title_font_color="#e4e8f1",
            legend_title_font_color="#e4e8f1"
        )
        fig_confirmados_idade.update_xaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_confirmados_idade.update_yaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_confirmados_idade.update_xaxes(title_font_family="Arial Bold")
        fig_confirmados_idade.update_layout(title_text='Casos confirmados por Faixa Etária')#,height=350,width=780)
        fig_confirmados_idade.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
        fig_confirmados_idade.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                          marker_line_width=1.5, opacity=0.6)

        return fig_confirmados_idade

######################### mapas

@app.callback(
    Output('fig_mapa','figure'),
    [Input('id_radioitens_mapa','value'),
    Input(component_id='filtro_datas', component_property='start_date'),
    Input(component_id='filtro_datas', component_property='end_date')]
)
def selecao(valor,start_date, end_date):
    mapbox_access_token ='pk.eyJ1IjoibGVpdGVjYWlvYnVlbm8iLCJhIjoiY2toODlkamJhMDA0bTJ3cjFlbXJjM3RtNCJ9.tkTUANVGBc5l-n0zn0tyKA'
    if valor=="id_obitos_mapa_radiobtn":
        temp = df_obitos[(df_obitos['DATA DO ÓBITO']>=start_date) & (df_obitos['DATA DO ÓBITO'] <=end_date)]
        temp.BAIRRO = temp.BAIRRO.str.upper()
        temp.BAIRRO = temp.BAIRRO.str.strip()
        temp.BAIRRO = temp['BAIRRO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        df_bairros_obitos = pd.DataFrame(temp.BAIRRO)
        df_bairros_obitos = temp.groupby(['BAIRRO'])['BAIRRO'].count()
        df_bairros_obitos = pd.DataFrame(df_bairros_obitos)
        df_bairros_obitos = df_bairros_obitos.rename(columns={'BAIRRO':'Variável'})
        df_bairros_obitos.reset_index(drop=False,inplace=True)
        df_bairros_bases_final2 = df_bairros_bases_final[['BAIRRO', 'lat', 'lon']]
        df_bairros_obitos_com_geo = pd.merge(df_bairros_obitos,df_bairros_bases_final2, how='left',on='BAIRRO')
        mapa_obitos = go.Figure(go.Scattermapbox(
                  lat=df_bairros_obitos_com_geo['lat'],
                  lon=df_bairros_obitos_com_geo['lon'],
                  mode='markers',
                #   text=df_bairros_obitos_com_geo[['BAIRRO','Variável']],#'Condições']],
                  hovertext=df_bairros_obitos_com_geo[['BAIRRO','Variável']],
                  hoverinfo="text",
                  marker=go.scattermapbox.Marker(
                      size=(df_bairros_obitos_com_geo[['Variável']]*100/df_bairros_obitos_com_geo['Variável'].max()),
                      color="#fc2c20"
                  ),
              ))
        mapa_obitos.update_layout(
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=-22.8205499,
                    lon=-43.0363389
                ),
                pitch=10,
                zoom=12
            )
        )
        mapa_obitos.update_layout(mapbox_style="mapbox://styles/mapbox/streets-v11")
        mapa_obitos.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return mapa_obitos
    if valor=="id_confirmados_obitos_radiobtn":
        temp = df_confirmados[(df_confirmados['NOTIFICAÇÃO']>=start_date) & (df_confirmados['NOTIFICAÇÃO'] <=end_date)]
        temp.BAIRRO = temp.BAIRRO.str.upper()
        temp.BAIRRO = temp.BAIRRO.str.strip()
        temp.BAIRRO = temp['BAIRRO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        df_bairros_confirmados = temp.groupby(['BAIRRO'])['BAIRRO'].count()
        df_bairros_confirmados = pd.DataFrame(df_bairros_confirmados)
        df_bairros_confirmados = df_bairros_confirmados.rename(columns={'BAIRRO':'Variável'})
        df_bairros_confirmados.reset_index(drop=False,inplace=True)
        df_bairros_bases_final2 = df_bairros_bases_final[['BAIRRO', 'lat', 'lon']]
        df_bairros_confirmados_com_geo = pd.merge(df_bairros_confirmados,df_bairros_bases_final2, how='left',on='BAIRRO')
        mapa_confirmados = go.Figure(go.Scattermapbox(
                  lat=df_bairros_confirmados_com_geo['lat'],
                  lon=df_bairros_confirmados_com_geo['lon'],
                  mode='markers',
                #   text=df_bairros_confirmados_com_geo[['BAIRRO','Variável']],#'Condições']],
                  hovertext=df_bairros_confirmados_com_geo[['BAIRRO','Variável']],
                  hoverinfo="text",
                  marker=go.scattermapbox.Marker(
                      size=(df_bairros_confirmados_com_geo[['Variável']]*100/df_bairros_confirmados_com_geo['Variável'].max()),
                      color="#ffa339"
                  ),
              ))
        mapa_confirmados.update_layout(
            hovermode='closest',
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=-22.8205499,
                    lon=-43.0363389
                ),
                pitch=10,
                zoom=12
            )
        )
        mapa_confirmados.update_layout(mapbox_style="mapbox://styles/mapbox/streets-v11")
        mapa_confirmados.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        return mapa_confirmados


################# Gráfico ao longo do tempo obitos e ocupacao de leitos ######################

@app.callback(
    Output('fig_grafico_temporal_2','figure'),
    [Input('id_radioitens_2','value'),
    Input(component_id='filtro_datas', component_property='start_date'),
    Input(component_id='filtro_datas', component_property='end_date')]
)
def selecao(valor,start_date, end_date):
    if valor=="id_obitos_radiobtn":
        temp = obitos_por_data[(obitos_por_data['DATA DO ÓBITO']>=start_date) & (obitos_por_data['DATA DO ÓBITO'] <=end_date)]
        # if end_date >= '2020/04/10':
        #     temp = obitos_por_data[(obitos_por_data['DATA DO ÓBITO']>=start_date) & (obitos_por_data['DATA DO ÓBITO'] <=end_date)]
        # else:
        #     temp = obitos_por_data
        fig_obitos_data = go.Figure(
            data=[
                go.Bar(
                    x = temp['DATA DO ÓBITO'],
                    y = temp['Casos obitos'],
                    hovertemplate=(
                        'Data de Notificação: %{x}'+
                        '<br>Quantidade de Óbitos: %{y}<extra></extra>'
                    )
                )
            ]
        )
        fig_obitos_data.update_traces(marker_color='#fc2c20', marker_line_color='#d00000',
                          marker_line_width=1.5, opacity=0.6)
        layout = fig_obitos_data.update_layout(
            paper_bgcolor='#000',
            plot_bgcolor='#000',
            xaxis_rangeslider_visible=True,
        )
        fig_obitos_data.update_layout(
            font_family="Courier New Bold",
            font_color="#e4e8f1",
            font_size=16,
            title_font_family="Times New Roman",
            title_font_color="#e4e8f1",
            legend_title_font_color="#e4e8f1"
        )
        fig_obitos_data.update_xaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_obitos_data.update_yaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_obitos_data.update_xaxes(title_font_family="Arial Bold")
        fig_obitos_data.update_layout(title_text='Óbitos pela data do óbito')
        fig_obitos_data.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
        return fig_obitos_data
    if valor=="id_leitos_radiobtn":
        temp = df_ocupacao_leitos_final[(df_ocupacao_leitos_final['Data']>=start_date) & (df_ocupacao_leitos_final['Data'] <=end_date)]
        fig_ocupacao = go.Figure()
        fig_ocupacao.add_trace(go.Scatter(
            x = temp['Data'],
            y = temp['UTI / CTI'],
            mode = 'lines+markers',
            name = 'UTI / CTI',
            hovertemplate=(
                        'Data: %{x}'+
                        '<br>Ocupação da UTI / CTI: %{y}<extra></extra>'
                    ),
            )
        )
        fig_ocupacao.add_trace(go.Scatter(
            x = temp['Data'],
            y = temp['Enfermaria'],
            mode = 'lines+markers',
            name = 'Enfermaria',
            hovertemplate=(
                        'Data: %{x}'+
                        '<br>Ocupação da Enfermaria: %{y}<extra></extra>'
                    ),
            )
        )

        layout = fig_ocupacao.update_layout(
            paper_bgcolor='#000',
            plot_bgcolor='#000',
            xaxis_rangeslider_visible=True,
        )
        fig_ocupacao.update_layout(
            font_family="Courier New Bold",
            font_color="#e4e8f1",
            font_size=16,
            title_font_family="Times New Roman",
            title_font_color="#e4e8f1",
            legend_title_font_color="#e4e8f1"
        )
        fig_ocupacao.update_xaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_ocupacao.update_yaxes(showgrid=False, linewidth=2, linecolor='black')
        fig_ocupacao.update_xaxes(title_font_family="Arial Bold")
        fig_ocupacao.update_layout(title_text='Taxa de ocupação ao longo do tempo')
        fig_ocupacao.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            ),
            legend = dict(
                  orientation="h",
                  yanchor="bottom",
                  y=1.03,
                  xanchor="right",
                  x=0.93,
                  ),
        )
        fig_ocupacao.update_layout(yaxis_tickformat = '.1%')
        return fig_ocupacao


################# Gráfico ao longo do tempo confirmados ######################

@app.callback(
    Output(component_id='fig_grafico_temporal_1', component_property='figure'),
    [Input(component_id='filtro_datas', component_property='start_date'),
    Input(component_id='filtro_datas', component_property='end_date')]
    )
def update_chart(start_date, end_date):
    temp = confirmados_por_data[(confirmados_por_data['NOTIFICAÇÃO']>=start_date) & (confirmados_por_data['NOTIFICAÇÃO'] <=end_date)]
    fig_confirmados_data = go.Figure(
        data=[
            go.Bar(
                x = temp['NOTIFICAÇÃO'],
                y = temp['Casos Confirmados'],
                hovertemplate=(
                    'Data de Notificação: %{x}'+
                    '<br>Quantidade de Casos Confirmados: %{y}<extra></extra>'
                ),

            )
        ]
    )
    fig_confirmados_data.update_traces(marker_color='#ffa339', marker_line_color='#fa7921',
                      marker_line_width=1.5, opacity=0.6)
    layout = fig_confirmados_data.update_layout(
        paper_bgcolor='#000',
        plot_bgcolor='#000',
        xaxis_rangeslider_visible=True,
    )
    fig_confirmados_data.update_layout(
        font_family="Courier New Bold",
        font_color="#e4e8f1",
        font_size=16,
        title_font_family="Times New Roman",
        title_font_color="#e4e8f1",
        legend_title_font_color="#e4e8f1"
    )
    fig_confirmados_data.update_xaxes(showgrid=False, linewidth=2, linecolor='black')
    fig_confirmados_data.update_yaxes(showgrid=False, linewidth=2, linecolor='black')
    fig_confirmados_data.update_xaxes(title_font_family="Arial Bold")
    fig_confirmados_data.update_layout(title_text='Casos confirmados pela data da notificação')
    fig_confirmados_data.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )
    return fig_confirmados_data

######## Tabela
@app.callback(
    Output(component_id='tabela_bairros_conf_obt', component_property='children'),
    [Input(component_id='filtro_datas', component_property='start_date'),
    Input(component_id='filtro_datas', component_property='end_date')]
    )
def update_chart(start_date, end_date):
    temp = df_confirmados[(df_confirmados['NOTIFICAÇÃO']>=start_date) & (df_confirmados['NOTIFICAÇÃO'] <=end_date)]
    temp.BAIRRO = temp.BAIRRO.str.upper()
    temp.BAIRRO = temp.BAIRRO.str.strip()
    temp.BAIRRO = temp['BAIRRO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    confirmados_por_genero3 = temp.groupby(['BAIRRO'])['BAIRRO'].count()
    confirmados_por_genero3 = pd.DataFrame(confirmados_por_genero3)
    confirmados_por_genero3 = confirmados_por_genero3.rename(columns={'BAIRRO':'Confirmados'})
    confirmados_por_genero3.reset_index(drop=False,inplace=True)
    temp2 = df_obitos[(df_obitos['DATA DO ÓBITO']>=start_date) & (df_obitos['DATA DO ÓBITO'] <=end_date)]
    temp2.BAIRRO = temp2.BAIRRO.str.upper()
    temp2.BAIRRO = temp2.BAIRRO.str.strip()
    temp2.BAIRRO = temp2['BAIRRO'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    confirmados_por_genero4 = temp2.groupby(['BAIRRO'])['BAIRRO'].count()
    confirmados_por_genero4 = pd.DataFrame(confirmados_por_genero4)
    confirmados_por_genero4 = confirmados_por_genero4.rename(columns={'BAIRRO':'Óbitos'})
    confirmados_por_genero4.reset_index(drop=False,inplace=True)
    df_por_bairros = pd.merge(confirmados_por_genero3,confirmados_por_genero4, on="BAIRRO",how='left')
    df_por_bairros.fillna(0,inplace=True)

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

    tabela_bairros = dash_table.DataTable(
        id='table_bairros',
        columns=[{"name": i, "id": i} for i in df_por_bairros.columns],
        data=df_por_bairros.to_dict('records'),
        style_cell={
            'textAlign': 'center',
            'backgroundColor': "#151a28",
            'whiteSpace': 'normal',
            'height': 'auto',
            'width': '{}%'.format(len(df_por_bairros.columns)),
            # 'padding': '5px'
            },
        style_as_list_view=True,
        sort_action='native',
        sort_mode='multi',
        sort_by=[],
        page_current=0,
        page_size=14,
        page_action='native',
        style_data_conditional=
            [
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
    return tabela_bairros

if __name__ == '__main__':
    app.run_server()
