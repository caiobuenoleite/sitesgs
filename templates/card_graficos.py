import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from plots.confirmados import fig_confirmados_data
from plots.obitos import fig_obitos_data
from plots.ocupacao import fig_ocupacao

card3 = html.Div(
    children = dbc.Col(
        [
            dbc.Row(
                [
                    dcc.Graph(
                        id = "fig_grafico_temporal_1",
                        figure = {},
                    ),
                    dcc.Graph(
                        id = "fig_grafico_temporal_2",
                        figure = {}
                    )

                ]
            ),
            dbc.Row(
                children= [
                    dbc.Col(

                    ),
                    dbc.Col(
                        dcc.RadioItems(
                            id='id_radioitens_2',
                            options=[
                                {'label': 'Óbitos confirmados', 'value': 'id_obitos_radiobtn'},
                                {'label': 'Ocupação de Leitos', 'value': 'id_leitos_radiobtn'},
                            ],
                            value='id_obitos_radiobtn',
                            labelStyle={'display': 'inline-block'},
                            inputStyle={"margin-right": "5px", "margin-left": "10px"},
                            style={'marginLeft':0 ,'fontSize':'14px'}
                        )
                    )

                ],
                style={"displat":"inline-block","text-align":"left",'marginTop':-60},
                align="end"
            )

        ]
    )

)
