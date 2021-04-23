
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

sg_logo = ['./assets/saogocalo_logo.png']

filtro_data = html.Div(
    dcc.DatePickerRange(
        id="filtro_datas",
        start_date_placeholder_text="",
        end_date_placeholder_text="",
        calendar_orientation='vertical',
        display_format='DD/MM/YYYY',
        start_date= '2020/03/01',
        end_date='2021/03/22'
        ),
    className="ml-auto flex-nowrap mt-3 mt-md-0"
)

calendario_png = html.Div(
    html.Img(src='./assets/hiclipart.com2.png', height="30px"),
    className="mr-2",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src='./assets/saogocalo_logo.png', height="45px")),
                    dbc.Col(dbc.NavbarBrand("Painel COVID-19 São Gonçalo, RJ", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://www.saogoncalo.rj.gov.br/",
        ),
        html.A(
            dbc.Row(
                [
                    calendario_png,
                    dbc.NavbarToggler(id="navbar-toggler"),
                    dbc.Collapse(filtro_data, id="navbar-collapse", navbar=True),
                ],
                align="center"
            ),
            className="ml-auto flex-nowrap mt-3 mt-md-0"
        )
    ],
    color="dark",
    dark=True,
)
