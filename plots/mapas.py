import plotly.graph_objects as go
from etl.mapas import df_bairros_obitos_com_geo, df_bairros_confirmados_com_geo

mapbox_access_token ='pk.eyJ1IjoibGVpdGVjYWlvYnVlbm8iLCJhIjoiY2toODlkamJhMDA0bTJ3cjFlbXJjM3RtNCJ9.tkTUANVGBc5l-n0zn0tyKA'
mapa_confirmados = go.Figure(go.Scattermapbox(
          lat=df_bairros_confirmados_com_geo['lat'],
          lon=df_bairros_confirmados_com_geo['lon'],
          mode='markers',
        #   text=df_bairros_confirmados_com_geo[['BAIRRO','Variável']],#'Condições']],
          hovertext=df_bairros_confirmados_com_geo[['BAIRRO','Variável']],
          hoverinfo="text",
          marker=go.scattermapbox.Marker(
              size=df_bairros_confirmados_com_geo[['Variável']]*100/2408,
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




mapa_obitos = go.Figure(go.Scattermapbox(
          lat=df_bairros_obitos_com_geo['lat'],
          lon=df_bairros_obitos_com_geo['lon'],
          mode='markers',
        #   text=df_bairros_obitos_com_geo[['BAIRRO','Variável']],#'Condições']],
          hovertext=df_bairros_obitos_com_geo[['BAIRRO','Variável']],
          hoverinfo="text",
          marker=go.scattermapbox.Marker(
              size=df_bairros_obitos_com_geo[['Variável']]*100/9,
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

