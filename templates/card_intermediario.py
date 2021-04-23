from dash_bootstrap_components._components.Card import Card
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from plots.tabela_bairros import tabela_bairros
from etl.bairros import df_por_bairros
import dash_table

card2 = html.Div(
    dbc.Row(
        children=[
            dbc.Col(
                dbc.Card(
                    [
                        dcc.Graph(
                            id = "fig_grafico_conf_genero",
                            figure = {}
                            ),
                        dcc.RadioItems(
                            id='id_radioitens',
                            options=[
                                {'label': 'Gênero', 'value': 'id_genero_radiobtn'},
                                {'label': 'Faixa Etária', 'value': 'id_faixaetaria_radiobtn'},
                                {'label': 'Por testagem', 'value': 'id_tipotestagem_radiobtn'},
                                {'label': 'Óbitos por Unidades notificantes', 'value': 'id_obtnotif_radiobtn'},
                            ],
                            value='id_genero_radiobtn',
                            labelStyle={'display': 'inline-block'},
                            inputStyle={"margin-right": "5px", "margin-left": "10px"},
                            style={'marginLeft':0 ,'fontSize':'12px'}
                        )
                    ],
                id="card_atributos"
                ),
            width=4
            ),
            dbc.Col(
                [
                    dcc.Graph(
                        id = "fig_mapa",
                        figure = {}
                        ),
                    dcc.RadioItems(
                        id='id_radioitens_mapa',
                        options=[
                            {'label': 'Casos Confirmados', 'value': 'id_confirmados_obitos_radiobtn'},
                            {'label': 'Óbitos Confirmados', 'value': 'id_obitos_mapa_radiobtn'},
                        ],
                        value='id_confirmados_obitos_radiobtn',
                        labelStyle={'display': 'inline-block'},
                        inputStyle={"margin-right": "5px", "margin-left": "10px"},
                        style={'marginLeft':0 ,'fontSize':'14px'}
                    )
                ],
            width=5
            ),
            dbc.Col(
                id='tabela_bairros_conf_obt',
                children={},
                style={'marginLeft':'-3mm'},
                width=3
            )
        ],
    ),
    id="card_intermediario",
)
