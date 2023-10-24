import plotly.io as pio
import plotly.express as px
import rasterio
from rasterio.plot import show
import pandas as pd
import requests

#this function visualized any given COG inside of a mapbox view
def visualize_COG(layer_url, zoom=1, center={"lat": 33.543682, "lon": -86.779633}):
    pio.renderers.default = 'iframe'
    styles_list = [
        "carto-darkmatter",
        "carto-positron",
        "open-street-map",
        "stamen-terrain",
        "stamen-toner",
        "stamen-watercolor",
        "white-bg"
    ]
    style = styles_list[1]
    # seed value, for mapbox to load in colab
    df = pd.DataFrame([[1001, 5.3],[1001, 5.3]])
    df.columns = ["flips", "unemp"]
    fig = px.choropleth_mapbox(
                                df, 
                                color='unemp',
                                color_continuous_scale="Viridis",
                                range_color=(0, 12),
                                mapbox_style=style,
                                center=center,
                                opacity=1,
                                zoom=zoom 
                              )
    fig.update_layout(
        mapbox_layers=[
            {
                "sourcetype": "raster",
                "source": [layer_url]
            }
          ])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(mapbox_style=style)
    fig.layout.mapbox.zoom = zoom
    fig.show()