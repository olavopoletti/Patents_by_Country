# %%
# Imports
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pycountry
from dash import dcc, html, Dash
import plotly as plt

app = Dash()
server = app.server

# %%
# ISO Countries names
iso2_to_iso3 = {c.alpha_2: c.alpha_3 for c in pycountry.countries}

# %%
# More readable number formats
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

# %%
# Load the dataset
df = pd.read_csv(r'dataset.csv').drop(columns=['Unnamed: 0'])
df['Year'] = df.Year.astype('str')
df['Pop_h'] = df.Population.apply(human_format)
df['Pats_h'] = df.Patents.apply(human_format)
df['GDP_h'] = df.GDP.apply(human_format)

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
    'range': [-100, 110000],
    'title': "GDP per Capita"
}
fig_dict['layout']['yaxis'] = {
    'range': [-1, 8.6],
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
                'method': 'animate',
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
        'showactive': False,
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
        'size': df[df.Year == f'{year}']['Patents'].div(35).values.tolist(),
        'color': 'White',
        'opacity': 1
    },
    'customdata':np.stack(
        (df[df.Year == f'{year}']['Pats_h'],
         df[df.Year == f'{year}']['Name'],
         df[df.Year == f'{year}']['Pop_h'],
         df[df.Year == f'{year}']['GDP_h'],
         df[df.Year == f'{year}']['Year'],
         ), 
        axis=-1
        ),
    'hovertemplate':
        '<b>%{customdata[1]}</b><br>'
        + '<b>%{customdata[4]}</b><br>'
        + 'Patents: %{customdata[0]}<br>'
        + 'Population: %{customdata[2]}<br>'
        + 'GDP per Capita: %{customdata[3]}<br>'
        + 'Patents Ratio: %{y:.2f}'
        '<extra></extra>'
    
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
        'text':[f'<b>{k}</b><b></b>'
                for k, i in zip(
                    df_temp['iso_3'].values.tolist(),
                    df_temp[ 'Year'].values.tolist()                                                
                )
                ],
        'textposition': ['middle center'],
        'textfont': dict(
            family='Segoe UI',
            size=12,
            color=['Black',],
            ),
        'marker': {
            'sizemode': 'area',
            'sizeref': 1,
            'size': df_temp['Patents'].div(35).values.tolist(),
            'color': 'White',
            'opacity': 1,

        },
        'customdata':np.stack(
                (df_temp['Pats_h'],
                df_temp['Name'],
                df_temp['Pop_h'],
                df_temp['GDP_h'],
                df_temp['Year'],
                ), 
                axis=-1
                ),
        'hovertemplate':
            '<b>%{customdata[1]}</b><br>'
            + '<b>%{customdata[4]}</b><br>'
            + 'Patents: %{customdata[0]}<br>'
            + 'Population: %{customdata[2]}<br>'
            + 'GDP per Capita: %{customdata[3]}<br>'
            + 'Patents Ratio: %{y:.2f}'
            '<extra></extra>'
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
            sizex=np.sqrt(row['Patents'] / df['Patents'].max()) * maxi * 0.02675 + maxi * 0.00135,
            sizey=np.sqrt(row['Patents'] / df['Patents'].max()) * maxi * 0.02675 + maxi * 0.00135,
            sizing='contain',
            opacity=.85,
            layer='above'
        )
    )

# %%
# Basic layout for the graphics
fig.update_layout(
    title='<b>Patents Granted</b>',
    font_family="Segoe UI",
    font_color="White",
    font_size=14,
    title_font_family="Segoe UI",
    title_font_color="White",
    title_font_size=45,
    title_y=1,
    title_x=0.5,
    showlegend=False,
    margin=dict(b=0,l=0,r=0,t=15),
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
        gridcolor='White',
        zeroline=True,
        zerolinecolor='White',
        zerolinewidth=3,
        showticklabels=True
        ),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    autosize=False,
    width=1250,
    height=650,
    hoverlabel=dict(
        align='right',
        bgcolor='White',
        bordercolor='White',
        font=dict(
            color='Black',
            family="Segoe UI",
            size=12
        )
    )
    )

# %%
# Show figure
fig.show()

# %%

app.layout = html.Div(
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

app.run_server(debug=False, host='0.0.0.0', port=8080)


