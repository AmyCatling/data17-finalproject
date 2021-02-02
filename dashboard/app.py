# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pyodbc
import base64

server = 'localhost,1433'
database = 'Northwind'
username = 'SA'
password = 'Passw0rd2018'
docker_Northwind = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server} ;SERVER='+server+'; DATABASE='+database+'; UID='+username+';PWD='+password)
cursor = docker_Northwind.cursor()



external_stylesheets = ['webpage.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = pd.read_sql('''
 SELECT c.CategoryName, AVG(p.UnitPrice) AS AveragePrice
 FROM Categories c
 JOIN Products p ON p.CategoryID = c.CategoryID
 GROUP by c.CategoryName
 ORDER BY AveragePrice DESC
''', docker_Northwind)



image_filename = 'SG-Logo-Black.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


#df['color'] = "#E13661"
fig = px.bar(df, x="CategoryName", y="AveragePrice", color_discrete_sequence=['#E13661'])

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Img(id='image_sparta', src='data:image/png;base64,{}'.format(encoded_image.decode())
         ),
    # html.H1(
    #     children='SPARTANS',
    #     style={
    #         'textAlign': 'center',
    #         'color': colors['text']
    #     }
    # ),

    html.Div(children='Sparta Global: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig,

    )

])

if __name__ == '__main__':
    app.run_server(debug=True)


    # html.Div(
    # html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))