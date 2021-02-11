import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import base64
from data_puller import AppData
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_table

t = AppData()
t.get_course_names()
t.get_student_behaviours()
t.set_chosen_course('test_21')
t.set_chosen_student('John Smith')
t.get_stu_info_table()
t.get_successful_applicants()
t.get_degree_classification_df()
t.get_annual_applicants_df()
t.get_avg_psy_pres_scores_df()
t.get_course_table()

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

fig = px.line(x=range(1,11), y=[list(t.stu_results_df[t.stu_results_df['behaviour_name'] == i]['score']) for i in t.behaviours],
              color_discrete_sequence=px.colors.qualitative.Bold, width=10, )
fig.update_xaxes(title='Week', ticks='inside', showline=True, linewidth=2, linecolor='#111111',
                 showgrid=True, gridwidth=0.1, gridcolor='#d6b8c0')
fig.update_yaxes(title='Score', ticks='inside', showline=True, linewidth=2, linecolor='#111111',
                 showgrid=True, gridwidth=0.1, gridcolor='#d6b8c0')
fig.update_layout(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor=colors['background'],
    font_color=colors['text'])
fig = customLegend(fig=fig, nameSwap={'wide_variable_0': t.behaviours[0], 'wide_variable_1':t.behaviours[1], 'wide_variable_2': t.behaviours[2],
                                        'wide_variable_3': t.behaviours[3], 'wide_variable_4': t.behaviours[4],'wide_variable_5': t.behaviours[5]})

applicants_bar = px.bar(data_frame=t.annual_applicants_df, x='Year', y="Number of Applicants",
                        title="Number of Applicants Annually")
applicants_bar.update_xaxes(type="category")

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
                html.A([
                        html.Img(id='image_sparta',

                                 src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                style = {'height': '150px',
                                         'width': '375px', 'display': 'inline-block'}
                                ), html.H1('Sparta Global Academy',
                                           style={'textAlign':'center', 'color':colors['text'], 'font-family':'sans-serif'})],
                    href='https://www.spartaglobal.com/'),
                html.Div([
                    # dash_table.DataTable(
                    #     id='ann_app',
                    #     columns=[{"name": i, "id": i} for i in t.annual_applicants_df.columns],
                    #     data=t.annual_applicants_df.to_dict('records'),
                    #     style_header={'fontWeight': 'bold', 'backgroundColor': '#E33661', 'textAlign': 'center',
                    #                   'font-family': 'sans-serif'},
                    #     style_cell={'backgroundColor': '#F093AB', 'textAlign': 'left', 'font-family': 'sans-serif'}
                    # ),
                    dcc.Graph(
                       id='ann_app',
                    figure=applicants_bar
                    ),

                    dash_table.DataTable(
                        id='deg_class',
                        columns=[{"name": i, "id": i} for i in t.degree_class_df.columns],
                        data=t.degree_class_df.to_dict('records'),
                        style_header={'fontWeight': 'bold', 'backgroundColor': '#E33661', 'textAlign': 'center',
                                      'font-family': 'sans-serif'},
                        style_cell={'backgroundColor': '#F093AB', 'textAlign': 'left', 'font-family': 'sans-serif'}
                    ),
                    dash_table.DataTable(
                        id='interview_scores',
                        columns=[{"name": i, "id": i} for i in t.scores_df.columns],
                        data=t.scores_df.to_dict('records'),
                        style_header={'fontWeight': 'bold', 'backgroundColor': '#E33661', 'textAlign': 'center',
                                      'font-family': 'sans-serif'},
                        style_cell={'backgroundColor': '#F093AB', 'textAlign': 'left', 'font-family': 'sans-serif'}
                    ),

                    dash_table.DataTable(
                        id='successful_percentage',
                        columns=[{"name": i, "id": i} for i in t.successful_percentage_df.columns],
                        data=t.successful_percentage_df.to_dict('records'),
                        style_header={'fontWeight': 'bold', 'backgroundColor': '#E33661', 'textAlign': 'center',
                                      'font-family': 'sans-serif'},
                        style_cell={'backgroundColor': '#F093AB', 'textAlign': 'left', 'font-family': 'sans-serif'}
                    ),




                ], style={'columnCount': 4}),
                html.Div([

                    html.Div(children=[html.Label(["Course",
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
                        }
                    )])]),

                html.Div(id='Course_change', children=[
                    html.Label(children=["Course Statistics",
                                dash_table.DataTable(
                                    id='course_stats',
                                    columns=[{"name": i, "id": i} for i in t.course_info_df.columns],
                                    data=t.course_info_df.to_dict('records'),
                                    style_header={'fontWeight': 'bold', 'backgroundColor': '#E33661',
                                                  'textAlign': 'center',
                                                  'font-family': 'sans-serif'},
                                    style_cell={'backgroundColor': '#F093AB', 'textAlign': 'left',
                                                'font-family': 'sans-serif'}
                                )], style={'columnCount': 2}),


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
                        }

                )])
                ])]),
                html.Div(id='change', children=[
                    dcc.Graph(
                        id='student_tracker',
                        figure=fig
                    ),
                    html.Div([
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
                    )], style={'columnCount': 2})
            ])])])



@app.callback(
    Output('Course_change', 'children'),
    Input('course', 'value'))
def change_students_choices(course_value):
    t.set_chosen_course(course_value)
    children = [html.Label(children=["Course Statistics"]),
                    html.Div([dash_table.DataTable(
                                    id='course_stats',
                                    columns=[{"name": i, "id": i} for i in t.course_info_df.columns],
                                    data=t.course_info_df.to_dict('records'),
                                    style_header={'fontWeight': 'bold', 'backgroundColor': '#E33661',
                                                  'textAlign': 'center',
                                                  'font-family': 'sans-serif'},
                                    style_cell={'backgroundColor': '#F093AB', 'textAlign': 'left',
                                                'font-family': 'sans-serif'}
                                )], style={'columnCount': 3}),


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
                        }

                )])
                ])]
    return children


@app.callback(
    Output('change', 'children'),
    Input('student', 'value'))
def update_student_table(student_value):
    t.set_chosen_student(student_value)
    fig = px.line(x=range(1,11),
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

