import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import base64
from data_puller import AppData
from dash.dependencies import Input, Output
#import plotly.graph_objects as go
import dash_table

t = AppData()
t.get_course_names()
t.get_student_behaviours()
t.set_chosen_course('test_21')
t.set_chosen_student('John Smith')
t.get_stu_info_table()


external_stylesheets = ['webpage.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

coolors = ['#E13661', '#6A1027', '#E75F81', '#EF95AB', '#350813', '#A0183A']

colors = {
    'background': '#FFFFFF',
    'text': '#111111'
}


def customLegend(fig, nameSwap):
    for i, dat in enumerate(fig.data):
        for elem in dat:
            if elem == 'name':
                fig.data[i].name = nameSwap[fig.data[i].name]
    return(fig)



image_filename = 'SG-Logo-Black.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

fig = px.line(x=[1,2,3,4,5,6,7,8,9,10], y=[list(t.stu_results_df[t.stu_results_df['behaviour_name'] == i]['score']) for i in t.behaviours],
              color_discrete_sequence=px.colors.qualitative.Bold, width=10, )
fig.update_xaxes(title='Week', ticks='inside', showline=True, linewidth=2, linecolor='#111111',
                 showgrid=True, gridwidth=0.1, gridcolor='#d6b8c0')
fig.update_yaxes(title='Score', ticks='inside', showline=True, linewidth=2, linecolor='#111111',
                 showgrid=True, gridwidth=0.1, gridcolor='#d6b8c0')
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])
fig = customLegend(fig=fig, nameSwap={'wide_variable_0': t.behaviours[0], 'wide_variable_1':t.behaviours[1], 'wide_variable_2': t.behaviours[2],
                                        'wide_variable_3': t.behaviours[3], 'wide_variable_4': t.behaviours[4],'wide_variable_5': t.behaviours[5]})


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
                html.A([
                        html.Img(id='image_sparta',

                                 src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                style = {'height': '150px',
                                         'width': '375px', 'display': 'inline-block'}
                                ), html.H1('Data17 Final Project',
                                           style={'textAlign':'center', 'color':colors['text'], 'font-family':'sans-serif'})],
                    href='https://www.spartaglobal.com/'),

                html.Div([

                    html.Div([html.Label(["Course",
                    dcc.Dropdown(
                            #multi=True,
                        id='course',
                        options=[{'label': i, 'value': i} for i in t.course_names],
                        value=t.chosen_course,
                        style={
                            'height': '40px',
                            'width': '750px',
                            'font-size': "100%",
                            'min-height': '10px',
                        },
                        className='six.columns'
                    )]),
                    html.Div([html.Label(["Student",
                    dcc.Dropdown(
                        id='student',
                        options=[{'label': i, 'value': i} for i in t.stu_names],
                        value=t.chosen_student,
                        style={
                            'height': '40px',
                            'width': '750px',
                            'font-size': "100%",
                            'min-height': '10px',
                            },
                            className='six.columns'

                    )])]),
                ]),
                html.Div(id='change', children=[
                    dcc.Graph(
                        id='student_tracker',
                        figure=fig
                    ),

                    dash_table.DataTable(
                        id='personal',
                        columns=[{"name": i, "id": i} for i in t.stu_info_table.columns],
                        data=t.stu_info_table.to_dict('records'),
                        style_header={'fontWeight': 'bold', 'backgroundColor': '#E33661', 'textAlign': 'center', 'font-family': 'sans-serif'},
                        style_cell={'backgroundColor': '#F093AB', 'textAlign': 'left', 'font-family': 'sans-serif'}

                    ),
                    dash_table.DataTable(
                        id='sparta',
                        columns=[{"name": i, "id": i} for i in t.other_info_table.columns],
                        data=t.other_info_table.to_dict('records'),
                        style_header={'fontWeight': 'bold', 'backgroundColor': '#E33661', 'textAlign': 'center', 'font-family': 'sans-serif'},
                        style_cell={'backgroundColor': '#F093AB', 'textAlign': 'left', 'font-family': 'sans-serif'}
                    )])
            ])])



@app.callback(
    Output('student', 'options'),
    Input('course', 'value'))
def change_students_choices(course_value):
    t.set_chosen_course(course_value)
    return [{'label': i, 'value': i} for i in t.stu_names]


@app.callback(
    Output('change', 'children'),
    Input('student', 'value'))
def update_student_table(student_value):
    t.set_chosen_student(student_value)
    fig = px.line(x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                  y=[list(t.stu_results_df[t.stu_results_df['behaviour_name'] == i]['score']) for i in t.behaviours],
                  color_discrete_sequence=px.colors.qualitative.Bold, width=10, )

    fig.update_xaxes(title='Week', ticks='inside', showline=True, linewidth=2, linecolor='#111111',
                     showgrid=True, gridwidth=0.1, gridcolor='#c2c2c2')
    fig.update_yaxes(title='Score', ticks='inside', showline=True, linewidth=2, linecolor='#111111',
                     showgrid=True, gridwidth=0.1, gridcolor='#c2c2c2')
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])
    fig = customLegend(fig=fig, nameSwap={'wide_variable_0': t.behaviours[0], 'wide_variable_1': t.behaviours[1],
                                          'wide_variable_2': t.behaviours[2],
                                          'wide_variable_3': t.behaviours[3], 'wide_variable_4': t.behaviours[4],
                                          'wide_variable_5': t.behaviours[5]})

    children = [
        dcc.Graph(
            id='student_tracker',
            figure=fig
        ),
        dash_table.DataTable(
            id='personal',
            columns=[{"name": i, "id": i} for i in t.stu_info_table.columns],
            data=t.stu_info_table.to_dict('records'),
            style_header={'fontWeight': 'bold', 'backgroundColor': '#E33661', 'textAlign': 'center', 'font-family':'sans-serif'},
            style_cell={'backgroundColor': '#F093AB', 'textAlign': 'left', 'font-family':'sans-serif'},

        ),
        dash_table.DataTable(
            id='sparta',
            columns=[{"name": i, "id": i} for i in t.other_info_table.columns],
            data=t.other_info_table.to_dict('records'),
            style_header = {'fontWeight': 'bold', 'backgroundColor': '#E33661', 'textAlign': 'center',
                        'font-family': 'sans-serif'},
            style_cell = {'backgroundColor': '#F093AB', 'textAlign': 'left', 'font-family': 'sans-serif'}

        )]
    return children






if __name__ == '__main__':
    app.run_server(debug=True)

