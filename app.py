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
app.layout = html.Div(
        children=[
        html.Img(src=app.get_asset_url('db.jpg'))
        ]              
)
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)


