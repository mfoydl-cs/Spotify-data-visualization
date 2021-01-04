import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

import plotly.express as px
from plotly.graph_objs import *
import plotly.graph_objects as go
import pandas
import math
import plotly.io as pio

pio.templates.default = "plotly_dark"


app = dash.Dash()

df = pandas.read_csv('project1_spotifyTop50s.csv')

'''
This function creates the Dataframe used in the left-hand scatterplot used for interactivity

Creates a dataframe consisting of:
    - Genre
    - Year
    - Number of times this genre appears in that year
    - Sum of popularity of all instances of this genre in the year
'''
def getAggDf():
    df2 = df[['top genre', 'year', 'pop']]

    data = {'top genre': [], 'year': [], 'count': [], 'pop': []}
    for genre in df2['top genre'].unique():
        for year in df2['year'].unique():
            df3 = df2[df2['year'] == year]
            df3 = df3[df3['top genre'] == genre]

            if len(df3) > 0:
                #print(df3)
                #print(genre, year,len(df3),df3['pop'].sum())
                data['top genre'].append(genre)
                data['year'].append(year)
                data['count'].append(len(df3))
                data['pop'].append(df3['pop'].sum())

    return pandas.DataFrame(data)

''' Creates the traces and figure for the Radar Chart '''
def getRadar(filterDf):
    categories = ['nrgy', 'val', 'dB', 'dnce', 'acous']

    popDf = filterDf.sort_values(by='pop', ascending=False)[:5]

    cat1 = popDf[categories[0]].tolist()
    cat2 = popDf[categories[1]].tolist()
    cat3 = popDf[categories[2]].tolist()
    cat4 = popDf[categories[3]].tolist()
    cat5 = popDf[categories[4]].tolist()
    titles = popDf['title'].tolist()

    fig = go.Figure()

    print(popDf)
    fig.add_trace(go.Scatterpolar(
        r=[cat1[0],cat2[0],cat3[0],cat4[0],cat5[0]],
        theta=categories,
        fill='toself',
        name=titles[0]
    ))
    fig.add_trace(go.Scatterpolar(
        r=[cat1[1], cat2[1], cat3[1], cat4[1], cat5[1]],
        theta=categories,
        fill='toself',
        name=titles[1]
    ))
    fig.add_trace(go.Scatterpolar(
        r=[cat1[2], cat2[2], cat3[2], cat4[2], cat5[2]],
        theta=categories,
        fill='toself',
        name=titles[2]
    ))
    fig.add_trace(go.Scatterpolar(
        r=[cat1[3], cat2[3], cat3[3], cat4[3], cat5[3]],
        theta=categories,
        fill='toself',
        name=titles[3]
    ))
    fig.add_trace(go.Scatterpolar(
        r=[cat1[4], cat2[4], cat3[4], cat4[4], cat5[4]],
        theta=categories,
        fill='toself',
        name=titles[4]
    ))

    fig.update_layout(showlegend=False,title="Top 5 Songs: Feature Comparison")
    return fig

    

app.layout = html.Div(id="main",children=[
    html.Div(id='title',children=[html.H1("Spotify Top 50's 2010-2019",style={"text-align":"center"})]),
    html.Div(id="top",children=[
        html.Div(id="top-left",children=[
            dcc.Graph(id='genre-plot', figure=px.scatter(getAggDf(), x='year', y='count', size='pop', title="Top Genre By Year",
                                                         hover_name='top genre', color='year',log_y=True ).update_layout(showlegend=False, dragmode='select').update_yaxes(showgrid=False))
        ], style={'flex': '1', "border-style": "solid", "border-width": "3px 1.5px 1.5px 3px"}),
        html.Div(id="top-right",children=[
            dcc.Graph(id='scatter_matrix_graph'),
            html.Div(children=[
                html.Label(["Color-By",
                    dcc.Dropdown(id='colorby', placeholder='Colorby', options=[{'label': 'Genre', 'value': 'top genre'}, {'label': 'Year', 'value': 'year'}],value="top genre")
                ])
            ],style={'padding-left':'5%','padding-right':'5%'})
        ], style={'flex': '1', "border-style": "solid", "border-width": "3px 3px 1.5px 1.5px"}),
    ], style={'display': 'flex','flex':'1'}),
    html.Div(id="bottom",children=[
        html.Div(id="bottom-left", children=[
            dcc.Graph(id='bar-chart')
        ], style={'flex': '1', "border-style": "solid", "border-width": "1.5px 1.5px 3px 3px"}),
        html.Div(id="bottom-right", children=[
            dcc.Graph(id='radar-plot')
        ], style={'flex': '1', "border-style": "solid", "border-width": "1.5px 3px 3px 1.5px"}),
    ], style={'display': 'flex', 'flex': '1'}),
], style={"background": "rgb(17, 17, 17)", "color": "lightgreen"})

@app.callback(
    Output('scatter_matrix_graph','figure'),
    Output('bar-chart','figure'),
    Output('radar-plot','figure'),
    Input('genre-plot','selectedData'),
    Input('colorby','value')
)
def callback(selection,colorby):
    filterDf = df
    genres = []
    years = []
    if selection and selection['points']:
        for point in selection['points']:
            genres.append(point['hovertext'])
            years.append(point['marker.color'])
        filterDf = filterDf[filterDf['top genre'].isin(genres) & filterDf['year'].isin(years)]

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    scatterFig = px.scatter_matrix(filterDf, dimensions=['nrgy', 'val', 'dB', 'dnce', 'acous'], title="Scatter Matrix of Song Features",color=colorby)
    barFig = px.bar(filterDf.sort_values(by='pop', ascending=False)[:10], x='title', y='pop',color='title', color_discrete_sequence=colors,title="Top 10 Songs by Popularity").update_layout(showlegend=False)
    
    radarFig = getRadar(filterDf)
    return [scatterFig,barFig,radarFig]

if __name__ == '__main__':
    app.run_server(debug=True)

