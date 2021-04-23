import dash_html_components as html
import dash_bootstrap_components as dbc
from etl.confirmados_data import valordiario_confirmados, datadiaria_confirmados
from etl.obitos_data import valordiario_obitos,datadiaria_obitos
from etl.obitos_data import valordiario_obitos,datadiaria_obitos
from etl.recuperados import valordiario_recuperados,datadiaria_recuperados

card1 = html.Div(
    children = dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        html.H2("Recuperados",id="classRecuperados"),
                        html.H2(""f"{valordiario_recuperados}",id="classRecuperadosNumero"),
                        dbc.Tooltip(
                            "Data: "f"{datadiaria_recuperados} \n\n *Valor referente ao número de indivíduos \nrecuperados entre os casos confirmados",
                            target="classRecuperadosNumero",
                            placement="bottom",
                            style={
                                "background-color": "#151a28",
                                "color": "#64ce6d",
                                'white-space':'pre'
                                }
                        )
                    ],
                    id="cardRecuperadosNum",
                ),
            ),
            dbc.Col(
                dbc.Card(
                    [
                        html.H2("Confirmados",id="classConfirmados"),
                        html.H2(""f"{str(valordiario_confirmados)}",id="classConfirmadosNumero"),
                        dbc.Tooltip(
                            "Data: "f"{datadiaria_confirmados}",
                            target="classConfirmadosNumero",
                            placement="bottom",
                            style={
                                "background-color": "#151a28",
                                "color": "#ffa339",
                                }
                        )
                    ],
                    id="cardConfirmadosNum"
                ),
            ),
            dbc.Col(
                dbc.Card(
                    children=[
                        html.H2("Óbitos Confirmados",id="classObitos"),
                        html.H2(""f"{valordiario_obitos}",id="classObitosNumero"),
                        dbc.Tooltip(
                            "Data: "f"{datadiaria_obitos}",
                            target="classObitosNumero",
                            placement="bottom",
                            style={
                                "background-color": "#151a28",
                                "color": "#fc2c20",
                                }
                        )
                    ],
                    id="cardObitosNum"
                ),
            ),
        ]
    ),
    id="ClassCard1"
)
