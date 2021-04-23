from etl.confirmados_genero import confirmados_por_genero
import plotly.express as px

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
