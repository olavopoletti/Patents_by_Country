# %%
# Imports
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pycountry
from dash import dcc, html, Dash
import plotly as plt

# %%
app = Dash(__name__)
server = app.server

html.Img(src=app.get_asset_url('db.jpg'))
app.layout = html.Div(
        children=[
                html.Div(
                        dcc.Graph(
                        #figure=fig,
                        style={
                                #"display": "block",
                                "margin-left": '40px',
                                "margin-right": '30px',
                                'margin-top': '40px',
                                'margin-bottom': '40px'
                                }
                        )
        )
        ],
        style={
        'verticalAlign':'middle',
        'textAlign': 'center',
        'width':'100%',
        'height':'100%',
        'top':'0px',
        'left':'0px',
        'z-index':'1000',
        'background-image': 'url(assets/db.jpg)',
        'position':'fixed',
        'background-size': 'contain',
        'background-size': 'cover',
        'background-size': '100%',
        'background-color': 'rgba(0, 0, 0, 0.55)',
        'background-blend-mode': 'darken',
        },                   
)              

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)


