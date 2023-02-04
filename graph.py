# %%
# Imports
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pycountry
from dash import dcc, html, Dash
import plotly as plt

# %%
# ISO Countries names
iso2_to_iso3 = {c.alpha_2: c.alpha_3 for c in pycountry.countries}

# %%
# Load the dataset
df = pd.read_csv(r'dataset.csv').drop(columns=['Unnamed: 0'])
df['Year'] = df.Year.astype('str')

# %%
# List years and countries
years = df.Year.unique().tolist()
countries = df.Name.unique().tolist()

# %%
# Make a figure
fig_dict = {
    'data': [],
    'layout': {},
    'frames': []
}

# %%
# Fill layout parameters
fig_dict['layout']['xaxis'] = {
    'range': [-200, 105000],
    'title': "GDP per Capita"
}
fig_dict['layout']['yaxis'] = {
    'range': [-2, 8],
    'title': 'Patents per 100,000 Population',
    #'type': 'log'
}
fig_dict['layout']['hovermode'] = 'closest'
fig_dict['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [
                    None,
                    {
                        'frame': {'duration':500, 'redraw': False},
                        'fromcurrent': True,
                        'transition': {
                            'duration': 300,
                            'easing': 'quadratic-in-out'
                        },
                    }
                ],
                'label': 'play',
                'method': 'animate'
            },
            {
                'args': [
                    [None],
                    {
                        'frame':{'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }
                ],
                'label': 'pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive':True,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        #'prefix': 'Year',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}
fig_dict["layout"]["sliders"] = [sliders_dict]


# %%
# Data
year = '1980'
data_dict = {
    'x': df[df.Year == f'{year}']['GDP'].values.tolist(),
    'y': df[df.Year == f'{year}']['Pat_100k'].values.tolist(),
    'mode': 'markers',
    'text': df[df.Year == f'{year}']['Name'].values.tolist(),
    'marker': {
        'sizemode': 'area',
        'sizeref': 1,
        'size': df[df.Year == f'{year}']['Patents'].div(70).values.tolist()
    }
}
fig_dict["data"].append(data_dict)

# %%
# Frames
for year in years:
    df_temp = df[df.Year == year]
    
    frame = {'data': [], 'name': str(year)}
    
    data_dict = {
        'x': df_temp['GDP'].values.tolist(),
        'y': df_temp['Pat_100k'].values.tolist(),
        'mode': 'markers+text',
        'text':[f'<b>{k}</b><br><b></b>'
                for k, i in zip(
                    df_temp['iso_3'].values.tolist(),
                    df_temp[ 'Year'].values.tolist()                                                
                )
                ],
        'textposition': ["middle center"],
        'textfont': dict(
            family="Segoe UI",
            size=10,
            color=['#FFAD00',],
            ),
        'marker': {
            'sizemode': 'area',
            'sizeref': 1,
            'size': df[df.Year == f'{year}']['Patents'].div(70).values.tolist()
        }
    }
    frame['data'].append(data_dict)
    
    fig_dict['frames'].append(frame)
    
    slider_step = {
        'args': [
            [year],
            {
                'frame': {'duration': 300, 'redraw': False},
                'mode': 'immediate',
                'transition': {'duration': 300}
            }
        ],
        'label': year,
        'method': 'animate'
    }
    sliders_dict['steps'].append(slider_step)


# %%
# Create figure object
fig = go.Figure(fig_dict)

# %%
# Add countries' flags for the 2021 data
dft = df[(df.Year == '2021')].sort_values(by='Patents', ascending=False)
for i, row in dft[0:8].iterrows():
    country_iso = row["iso_2"]
    
    min_dim = df[['Patents']].max().idxmax()
    maxi = df[min_dim].max()

    fig.add_layout_image(
        dict(
            source=f'assets/{country_iso}.png',
            xref='x',
            yref='y',
            xanchor='center',
            yanchor='middle',
            x=row['GDP'],
            y=row['Pat_100k'],
            sizex=np.sqrt(row['Patents'] / df['Patents'].max()) * maxi * 0.017 + maxi * 0.000725,
            sizey=np.sqrt(row['Patents'] / df['Patents'].max()) * maxi * 0.017 + maxi * 0.000725,
            sizing='contain',
            opacity=.75,
            layer='above'
        )
    )

# %%
# Basic layout for the graphics
fig.update_layout(
    title='Patents Granted',
    font_family="Segoe UI",
    font_color="Black",
    font_size=14,
    title_font_family="Segoe UI",
    title_font_color="#000000",
    title_font_size=18,
    showlegend=False,
    margin=dict(b = 10,l= 20,r=10,t=50),
    xaxis=dict(
        showgrid=False,
        gridcolor='DarkGrey',
        zeroline=False,
        zerolinecolor='White',
        zerolinewidth=2,
        showticklabels=True,
        ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#C5B4E3',
        zeroline=True,
        zerolinecolor='#C5B4E3',
        zerolinewidth=2,
        showticklabels=True
        ),
    plot_bgcolor='White',
    paper_bgcolor='White',
    autosize=False,
    width=1300,
    height=650,
    )

# %%
# Show figure
fig.show()

# %%
app = Dash()
server = app.server
app.layout = html.Div([
    
    #html.H1('Patents Granted'),
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=False)


