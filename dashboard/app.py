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
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# CONNECT TO DB -- NEEDS TO BE CONFIG'D
server = 'localhost,1433'
database = 'Northwind'
username = 'SA'
password = 'Passw0rd2018'
docker_Northwind = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server} ;SERVER='+server+'; DATABASE='+database+'; UID='+username+';PWD='+password)
cursor = docker_Northwind.cursor()

# CSS
external_stylesheets = ['webpage.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}

# GET CATEGORY NAMES AND AVG PRICES FROM NORTHWIND
df = pd.read_sql('''
 SELECT c.CategoryName, AVG(p.UnitPrice) AS AveragePrice
 FROM Categories c
 JOIN Products p ON p.CategoryID = c.CategoryID
 GROUP by c.CategoryName
 ORDER BY AveragePrice DESC
''', docker_Northwind)


# GET SPARTAN NAMES FROM TEST TABLE
df2 = pd.read_sql('''
    SELECT * FROM test
''', docker_Northwind)
available_indicators = []
for name in df2['name']:
    available_indicators.append(name)
dftemp = df2.set_index('name')


#SPARTA LOGO
image_filename = 'SG-Logo-Black.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

fig = px.line(x=dftemp.columns, y=dftemp.values[0], color_discrete_sequence=['#E13661'])
fig.update_xaxes(title='Weeks', ticks='inside', showline=True, linewidth=2, linecolor='#E13661',
                 showgrid=True, gridwidth=0.1, gridcolor='#d6b8c0')
fig.update_yaxes(title='Score', ticks='inside', showline=True, linewidth=2, linecolor='#E13661',
                 showgrid=True, gridwidth=0.1, gridcolor='#d6b8c0')
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']

)


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
            html.Img(id='image_sparta',
                     src='data:image/png;base64,{}'.format(encoded_image.decode()),
                    style = {'height': '75px',
                             'width': '187px', 'display': 'inline-block'}
                    ), html.H1('Data17 Final Project',
                               style={'textAlign':'center', 'color':colors['text'], 'font-family':'sans-serif'}),

    html.Div([
        dcc.Dropdown(
                multi=True,
            id='student',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value=available_indicators[0],
            style={
                'height': '40px',
                'width': '750px',
                'font-size': "100%",
                'min-height': '10px',
                }
        )
    ]),
    dcc.Graph(
        id='student_tracker',
        figure=fig,

    )
])

@app.callback(
    Output('student_tracker', 'figure'),
    Input('student', 'value'))
def update_graph(student_value):
    dff = df2[df2['name'] == student_value]
    dff = dff.set_index('name')
    yv = dff.values[0]
    fig = px.line(x=dff.columns, y=yv)
    fig.update_xaxes(title='Weeks', ticks='inside', showline=True, linewidth=2, linecolor='#E13661',
                     showgrid=True, gridwidth=0.1, gridcolor='#d6b8c0')
    fig.update_yaxes(title='Score', ticks='inside', showline=True, linewidth=2, linecolor='#E13661',
                     showgrid=True, gridwidth=0.1, gridcolor='#d6b8c0')
    return fig

# def update_graph(student_value):
#     if type(student_value) == list:
#         if len(student_value) >= 1:
#             dff = df2[df2['name'] == student_value[0]]
#             for name in student_value[1:]:
#                 new_dff
#                 dff = pd.concat(dff, df2[df2['name'] == name]x)
#
#
#         else:
#             dff = df2[df2['name'] == student_value]
#     else:
#         dff = df2[df2['name'] == student_value]
#
#     print(dff)
#
#     dff = dff.set_index('name')
#     yv = dff.values[0]
#     fig = px.line(x=dff.columns, y=yv)
#     fig.update_xaxes(title='Weeks', ticks='inside', showline=True, linewidth=2, linecolor='#E13661',
#                      showgrid=True, gridwidth=0.1, gridcolor='#d6b8c0')
#     fig.update_yaxes(title='Score', ticks='inside', showline=True, linewidth=2, linecolor='#E13661',
#                      showgrid=True, gridwidth=0.1, gridcolor='#d6b8c0')
#
#     return fig





if __name__ == '__main__':
    app.run_server(debug=True)





