import plotly.graph_objects as go
from etl.confirmados_data import confirmados_por_data
import datetime as dt

confirmados_por_data = confirmados_por_data[confirmados_por_data['NOTIFICAÇÃO']<=dt.datetime.today()]
fig_confirmados_data = go.Figure(
    data=[
        go.Bar(
            x = confirmados_por_data['NOTIFICAÇÃO'],
            y = confirmados_por_data['Casos Confirmados'],
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
