import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import pyodbc
import base64
from dash.dependencies import Input, Output
import plotly.graph_objects as go


class AppData:

    def __init__(self):
        self.server = 'localhost,1433'
        self.database = 'test_Sparta_Db'
        self.username = 'SA'
        self.password = 'Passw0rd2018'
        self.docker = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server} ;SERVER=' + self.server + '; DATABASE=' + self.database + '; UID=' + self.username + ';PWD=' + self.password)
        self.cursor = self.docker.cursor()
        self.get_course_names()
        self.get_student_behaviours()


    def get_course_names(self):
        self.course_names = list(pd.read_sql('''
                                        SELECT course_name FROM Courses
                                        ''', self.docker)['course_name'])
        #print(self.course_names)

    def get_student_behaviours(self):
        self.behaviours = list(pd.read_sql('''
                                                SELECT behaviour_name FROM Behaviours
                                                ''', self.docker)['behaviour_name'])
        #print(self.behaviours)

    # get a df of results for one student, specified by name, returns all behaviours, all weeks
    def get_results_df_one_stu(self):
        self.stu_results_df = pd.read_sql(f"""
                                        SELECT Applicants.name, Behaviours.behaviour_name, Behaviours.behaviour_id,
                                        Weekly_Results.week_number, Weekly_Results.score 
                                        FROM Weekly_Results 
                                        INNER JOIN Applicants ON Applicants.applicant_id = Weekly_Results.applicant_id
                                        INNER JOIN Behaviours ON Behaviours.behaviour_id = Weekly_Results.behaviour_id
                                        WHERE Applicants.name = '{self.chosen_student}' 
                                        """, self.docker)
        #print(self.stu_results_df.to_string())

    # get a df of results for one student, specified by name, returns numerical results from sparta day (psychometric, presentation)
    def get_sparta_day_results_one_stu(self):
        self.sparta_day_results = pd.read_sql(f"""
                                                SELECT Applicants.name, Sparta_Day_Assessment.psychometric_score, 
                                                Sparta_Day_Assessment.presentation_score
                                                FROM Applicants
                                                INNER JOIN Sparta_Day_Assessment ON Sparta_Day_Assessment.applicant_id =
                                                Applicants.applicant_id
                                                WHERE Applicants.name = '{self.chosen_student}'
                                                """, self.docker)
        #print(self.sparta_day_results.to_string())


    def get_stu_names(self):
        self.stu_names = list(pd.read_sql(f'''
                                            SELECT Applicants.name FROM Student 
                                            JOIN Courses ON Student.course_id = Courses.course_id
                                            JOIN Applicants ON Student.applicant_id = Applicants.applicant_id
                                            WHERE Courses.course_name = '{self.chosen_course}'
                                            ''', self.docker)['name'])
        self.set_chosen_student(self.stu_names[0])

    def set_chosen_course(self, course_name):
        self.chosen_course = course_name
        self.get_stu_names()


    def set_chosen_student(self, student_name):
        self.chosen_student = student_name
        self.get_results_df_one_stu()
        self.get_sparta_day_results_one_stu()

t = AppData()

t.get_course_names()
t.get_student_behaviours()
t.set_chosen_course('test_21')
t.set_chosen_student('John Smith')


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
              color_discrete_sequence=coolors, width=10, )
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
            html.Img(id='image_sparta',
                     src='data:image/png;base64,{}'.format(encoded_image.decode()),
                    style = {'height': '75px',
                             'width': '187px', 'display': 'inline-block'}
                    ), html.H1('Data17 Final Project',
                               style={'textAlign':'center', 'color':colors['text'], 'font-family':'sans-serif'}),

    html.Div([
        dcc.Dropdown(
                #multi=True,
            id='student',
            options=[{'label': i, 'value': i} for i in t.stu_names],
            value=t.chosen_student,
            style={
                'height': '40px',
                'width': '750px',
                'font-size': "100%",
                'min-height': '10px',
                }
        ),
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
    Input('course', 'value'))
def update_student_choice(student_value, course_value):
    t.set_chosen_course(course_value)
    t.set_chosen_student(student_value)
    fig = px.line(x=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                  y=[list(t.stu_results_df[t.stu_results_df['behaviour_name'] == i]['score']) for i in t.behaviours],
                  color_discrete_sequence=coolors, width=10, )

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
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)

