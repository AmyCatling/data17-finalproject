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
t.get_monthly_applicants_df()
t.get_avg_psy_pres_scores_df()
t.get_course_table()
t.get_combo_table()

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

applicants_bar = px.bar(data_frame=t.monthly_applicants_df, x='Month', y="Number of Applicants",
                        color_discrete_sequence=["#E13661"])

applicants_bar.update_xaxes(type="category")

degree_bar = px.bar(data_frame=t.degree_class_df, x="Degree Classification", y="Count",
                    color_discrete_sequence=["#E13661"])
degree_bar.update_xaxes(type="category")

app.layout = html.Div(style={'backgroundColor': colors['background'], "vertical-align": "middle"}, children=[
                html.A([
                        html.Img(id='image_sparta',

                                 src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                style = {'height': '150px',
                                         'width': '375px', 'display': 'inline-block'}
                                ), html.H1('Sparta Global Academy',
                                           style={'textAlign': 'center', "font-family": "sans-serif",
                                                  'color': colors['text']})],
                    href='https://www.spartaglobal.com/'),
                html.Div([
                        html.Div([
                            html.H3("Number of Applicants Monthly in 2019",
                                    style={'textAlign': 'center', "font-family": "sans-serif", "margin": "50px"}),
                            dcc.Graph(id='g1', figure=applicants_bar)
                        ]),

                        html.Div([
                            html.H3("Distribution of Degree Classification of Successful Applicants",
                                    style={'textAlign': 'center', "font-family": "sans-serif", "margin": "50px"}),
                            dcc.Graph(id='g2', figure=degree_bar)

                    ])], style={'columnCount': 2, "verticalAlign":"middle", "margin": "50px"}),

                html.Div([
                    dash_table.DataTable(
                        id='interview_scores',
                        columns=[{"name": i, "id": i} for i in t.scores_df.columns],

                        data=t.scores_df.to_dict('records'),
                        style_header={'fontWeight': 'bold', 'backgroundColor': '#E13661', 'textAlign': 'center',
                                      'font-family': 'sans-serif'},
                        style_cell={'backgroundColor': '#F4B8C7', 'textAlign': 'left', 'font-family': 'sans-serif'}
                    ),
                    ], style={'margin': '50px'}),




                html.Div([

                    html.Div([html.H3("Select course:", style={"font-family": "sans-serif"}),
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
                            'font-family': 'sans-serif',
                            'margin': '50px'
                        }
                    )])]),

                html.Div(id='Course_change', children=[
                    html.H3("Course Statistics",
                            style={"textAlign":"center", "font-family": "sans-serif", "margin": "50px"}),
                                dash_table.DataTable(
                                    id='course_stats',
                                    columns=[{"name": i, "id": i} for i in t.course_info_df.columns],
                                    data=t.course_info_df.to_dict('records'),
                                    style_header={'fontWeight': 'bold', 'backgroundColor': '#E13661',
                                                  'textAlign': 'center',
                                                  'font-family': 'sans-serif'},
                                    style_cell={'backgroundColor': '#F4B8C7', 'textAlign': 'left',
                                                'font-family': 'sans-serif'}
                                ),


                html.Div([html.H3("Select student:",
                                  style={"font-family": "sans-serif", "margin": "50px"}),
                dcc.Dropdown(
                    id='student',
                    options=[{'label': i, 'value': i} for i in t.stu_names],
                    value=t.chosen_student,
                    style={
                        'height': '40px',
                        'width': '750px',
                        'font-size': "100%",
                        'min-height': '10px',
                        'font-family': 'sans-serif',
                        'margin': '50px'

                        }

                )])
                ]),
                html.Div(id='change', children=[
                    html.Div([
                    dcc.Graph(
                        id='student_tracker',
                        figure=fig
                    )], style={'columnCount': 1}),
                    html.Div([
                    dash_table.DataTable(
                        id='personal',
                        columns=[{"name": i, "id": i} for i in t.stu_info_table.columns],
                        data=t.stu_info_table.to_dict('records'),
                        style_header={'fontWeight': 'bold', 'backgroundColor': '#E13661', 'textAlign': 'center', 'font-family': 'sans-serif'},
                        style_cell={'backgroundColor': '#F4B8C7', 'textAlign': 'left', 'font-family': 'sans-serif'}

                    ),
                    dash_table.DataTable(
                        id='sparta',
                        columns=[{"name": i, "id": i} for i in t.other_info_table.columns],
                        data=t.other_info_table.to_dict('records'),
                        style_header={'fontWeight': 'bold', 'backgroundColor': '#E13661', 'textAlign': 'center', 'font-family': 'sans-serif'},
                        style_cell={'backgroundColor': '#F4B8C7', 'textAlign': 'left', 'font-family': 'sans-serif'}
                    )], style={'columnCount': 2, 'margin':'50px'}, )
            ])])


@app.callback(
    Output('Course_change', 'children'),
    Input('course', 'value'))
def change_students_choices(course_value):
    t.set_chosen_course(course_value)
    children = [html.Div(id='Course_change', children=[
        html.H3("Course Statistics", style={"textAlign": "center", "font-family": "sans-serif", "margin": "50px"}),
        dash_table.DataTable(
            id='course_stats',
            columns=[{"name": i, "id": i} for i in t.course_info_df.columns],
            data=t.course_info_df.to_dict('records'),
            style_header={'fontWeight': 'bold', 'backgroundColor': '#E13661',
                          'textAlign': 'center',
                          'font-family': 'sans-serif'},
            style_cell={'backgroundColor': '#F4B8C7', 'textAlign': 'left',
                        'font-family': 'sans-serif'}
        ),

        html.Div([html.H3("Select student:", style={"font-family": "sans-serif", "margin": "50px"}),
                  dcc.Dropdown(
                      id='student',
                      options=[{'label': i, 'value': i} for i in t.stu_names],
                      value=t.chosen_student,
                      style={
                          'height': '40px',
                          'width': '750px',
                          'font-size': "100%",
                          'min-height': '10px',
                          'font-family': 'sans-serif',
                          'margin': '50px'
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
        html.Div([
        dcc.Graph(
            id='student_tracker',
            figure=fig
        )]),
        html.Div([
            dash_table.DataTable(
                id='personal',
                columns=[{"name": i, "id": i} for i in t.stu_info_table.columns],
                data=t.stu_info_table.to_dict('records'),
                style_header={'fontWeight': 'bold', 'backgroundColor': '#E13661', 'textAlign': 'center',
                              'font-family': 'sans-serif'},
                style_cell={'backgroundColor': '#F4B8C7', 'textAlign': 'left', 'font-family': 'sans-serif'}

            ),
            dash_table.DataTable(
                id='sparta',
                columns=[{"name": i, "id": i} for i in t.other_info_table.columns],
                data=t.other_info_table.to_dict('records'),
                style_header={'fontWeight': 'bold', 'backgroundColor': '#E13661', 'textAlign': 'center',
                              'font-family': 'sans-serif'},
                style_cell={'backgroundColor': '#F4B8C7', 'textAlign': 'left', 'font-family': 'sans-serif'}
            )], style={'columnCount': 2, 'margin': '50px'}, )]
    return children






if __name__ == '__main__':
    app.run_server(debug=True)

