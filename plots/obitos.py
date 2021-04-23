import plotly.graph_objects as go
from etl.obitos_data import obitos_por_data
from datetime import datetime

obitos_por_data = obitos_por_data[obitos_por_data['DATA DO ÓBITO']>="17/03/2020"]
fig_obitos_data = go.Figure(
    data=[
        go.Bar(
            x = obitos_por_data['DATA DO ÓBITO'],
            y = obitos_por_data['Casos obitos'],
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
