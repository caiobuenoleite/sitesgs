from etl.ocupacao import df_ocupacao_leitos_final
import plotly.graph_objects as go

fig_ocupacao = go.Figure()
fig_ocupacao.add_trace(go.Scatter(
    x = df_ocupacao_leitos_final['Data'],
    y = df_ocupacao_leitos_final['UTI / CTI'],
    mode = 'lines+markers',
    name = 'UTI / CTI',
    hovertemplate=(
                'Data: %{x}'+
                '<br>Ocupação da UTI / CTI: %{y}<extra></extra>'
            ),
    )
)
fig_ocupacao.add_trace(go.Scatter(
    x = df_ocupacao_leitos_final['Data'],
    y = df_ocupacao_leitos_final['Enfermaria'],
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
