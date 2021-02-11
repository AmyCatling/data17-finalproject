import plotly.express as px
import pandas as pd
import pyodbc
import base64
import datetime


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

    def get_student_behaviours(self):
        self.behaviours = list(pd.read_sql('''
                                                SELECT behaviour_name FROM Behaviours
                                                ''', self.docker)['behaviour_name'])


    def get_results_df_one_stu(self):
        self.stu_results_df = pd.read_sql(f"""
                                        SELECT Applicants.name, Behaviours.behaviour_name, Behaviours.behaviour_id,
                                        Weekly_Results.week_number, Weekly_Results.score 
                                        FROM Weekly_Results 
                                        INNER JOIN Applicants ON Applicants.applicant_id = Weekly_Results.applicant_id
                                        INNER JOIN Behaviours ON Behaviours.behaviour_id = Weekly_Results.behaviour_id
                                        WHERE Applicants.name = '{self.chosen_student}' 
                                        """, self.docker)

    def get_sparta_day_results_one_stu(self):
        self.sparta_day_results = pd.read_sql(f"""
                                                SELECT Applicants.name, Sparta_Day_Assessment.psychometric_score, 
                                                Sparta_Day_Assessment.presentation_score
                                                FROM Applicants
                                                INNER JOIN Sparta_Day_Assessment ON Sparta_Day_Assessment.applicant_id =
                                                Applicants.applicant_id
                                                WHERE Applicants.name = '{self.chosen_student}'
                                                """, self.docker)


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
        self.get_course_table()


    def set_chosen_student(self, student_name):
        self.chosen_student = student_name
        self.get_results_df_one_stu()
        self.get_sparta_day_results_one_stu()
        self.get_other_info_table()
        self.get_stu_info_table()

    def get_stu_strengths(self):
        self.strengths_list = list(pd.read_sql(f"""
        SELECT strength_name FROM Strengths
        INNER JOIN Strength_junction_table ON Strengths.strength_id = Strength_junction_table.strength_id
        INNER JOIN Applicants ON Strength_junction_table.applicant_id = Applicants.applicant_id
        WHERE Applicants.name = '{self.chosen_student}'
        """, self.docker)['strength_name'])

    def get_stu_weaknesses(self):
        self.weaknesses_list = list(pd.read_sql(f"""
        SELECT weakness_name FROM Weaknesses
        INNER JOIN Weakness_junction_table ON Weaknesses.weakness_id = Weakness_junction_table.weakness_id
        INNER JOIN Applicants ON Weakness_junction_table.applicant_id = Applicants.applicant_id
        WHERE Applicants.name = '{self.chosen_student}'
        """, self.docker)['weakness_name'])

    def get_stu_info_table(self):
        self.stu_info_table = pd.read_sql(f"""
        SELECT Applicants.email AS "Email Address", University_Details.university_name AS "University", 
        Degree_Grade.classification AS "Degree Classification", Staff.staff_name AS "Trainer", 
        Academies.academy_location AS "Academy"
        FROM Applicants
        INNER JOIN University_Details ON University_Details.university_id = Applicants.university_id
        INNER JOIN Degree_Grade ON Degree_Grade.degree_grade_id = Applicants.degree_grade_id
        INNER JOIN Staff ON Staff.staff_id = Applicants.staff_id
        INNER JOIN Sparta_Day_Assessment ON Sparta_Day_Assessment.applicant_id = Applicants.applicant_id
        INNER JOIN Academies ON Sparta_Day_Assessment.academy_id = Academies.academy_id
        WHERE Applicants.name = '{self.chosen_student}'
        """, self.docker)



    def get_other_info_table(self):
        self.other_info_table = pd.read_sql(f"""
        SELECT Sparta_Day_Assessment.psychometric_score AS "Psychometric Test Score", 
        Sparta_Day_Assessment.presentation_score AS "Presentation Test Score"
        FROM Applicants
        INNER JOIN Sparta_Day_Assessment ON Sparta_Day_Assessment.applicant_id = Applicants.applicant_id
        WHERE Applicants.name = '{self.chosen_student}'
        """, self.docker)
        self.get_stu_weaknesses()
        self.get_stu_strengths()

        self.other_info_table['Strengths'] = str(self.strengths_list)[1:-1].replace("'", "")
        self.other_info_table['Weaknesses'] = str(self.weaknesses_list)[1:-1].replace("'", "")

    def get_successful_applicants(self):
        successful = pd.read_sql("""SELECT COUNT(result) AS "successful" FROM Sparta_day_interview WHERE result =1""", self.docker)["successful"][0]

        all = pd.read_sql("""SELECT COUNT(*) AS "Total" FROM Applicants""", self.docker)["Total"][0]

        self.successful_percentage = str(round((float(successful) / float(all) * 100), 2)) + '%'
        self.successful_percentage_df = pd.DataFrame([self.successful_percentage])
        self.successful_percentage_df.columns = ["Percentage of Successful Applicants"]



    # distribution of degree classification for successful applicants
    def get_degree_classification_df(self):
        self.degree_class_df = pd.read_sql("""
                                           SELECT d.classification AS "Degree Classification", 
                                           COUNT(a.degree_grade_id) AS "Count" 
                                           FROM Applicants a
                                           JOIN Degree_Grade d ON a.degree_grade_id = d.degree_grade_id
                                           JOIN Sparta_day_interview i ON i.applicant_id = a.applicant_id
                                           WHERE i.result = 1
                                           GROUP BY a.degree_grade_id, d.classification
                                            """, self.docker)
    # number of applicants each year
    def get_monthly_applicants_df(self):
        self.monthly_applicants_df = pd.read_sql("""
                                                SELECT MONTH(sparta_day_date) AS "Month", 
                                                COUNT(MONTH(sparta_day_date)) AS "Number of Applicants"
                                                FROM Sparta_day_assessment 
                                                GROUP BY MONTH(sparta_day_date)
                                                """, self.docker)
        months = []
        for month in self.monthly_applicants_df['Month']:
            months.append(datetime.datetime.strptime(str(month), "%m").strftime("%b"))
        self.monthly_applicants_df['Month'] = months

    # avg psychometric and pres scores for successful applicants
    def get_avg_psy_pres_scores_df(self):
        self.scores_df = pd.read_sql("""
                                    SELECT AVG(psychometric_score) AS "Psychometric Test", 
                                    AVG(presentation_score) AS "Presentation"
                                    FROM Sparta_day_assessment s
                                    JOIN Applicants a ON a.applicant_id = s.applicant_id
                                    JOIN Sparta_day_interview i ON i.applicant_id = a.applicant_id
                                    WHERE i.result=1
                                    """, self.docker)



        # self.scores_df = self.scores_df.T
        #
        # self.scores_df.columns = ["Average Score"]
        # self.scores_df['Assessment'] = ['Psychometric', 'Presentation']
        #
        # self.scores_df = self.scores_df[["Assessment", "Average Score"]]




    def get_course_table(self):
        self.course_info_df = pd.read_sql(f"""
                                            SELECT c.course_name AS "Course", s.staff_name AS "Trainer", 
                                            COUNT(a.applicant_id) AS "Number of Trainees"
                                            FROM Courses c
                                            JOIN Staff s ON s.staff_id = c.staff_id
                                            JOIN Applicants a ON s.staff_id = a.staff_id
                                            WHERE c.course_name = '{self.chosen_course}'
                                            GROUP BY c.course_name, s.staff_name
                                            """, self.docker)

        # percentage of students that have graduated
        # number_graduated = pd.read_sql(f"""
        #                                 SELECT COUNT(*) AS "Count"
        #                                 FROM Courses c
        #                                 JOIN Students s ON s.course_id = c.course_id
        #                                 WHERE  c.course_name = '{self.chosen_course}' AND s.graduated = "y"
        #                                 """, self.docker)["Count"][0]
        # all = pd.read_sql(f"""
        #                     SELECT COUNT(*) AS "Count"
        #                     FROM Students s
        #                     JOIN Courses c ON c.course_id = s.course_id
        #                     WHERE c.course_name = '{self.chosen_course}'
        #                 """)
        # percentage_graduated = str(round((float(number_graduated)/float(all)*100), 2)) + '%'
        # self.course_info_df["Percentage of Graduated Trainees"] = percentage_graduated

        # need to add course start date and end date




    def get_combo_table(self):

        self.scores_df["Percentage of Applicants Accepted"] = [self.successful_percentage]
        self.scores_df.columns = ["Average Psychometric Test Score", "Average Presentation Score", "Percentage of Applicants Accepted"]
        # print(self.scores_df)

        # percentage who complete the course
        # graduated = pd.read_sql("""
        #             SELECT COUNT(*) AS "Count" FROM STUDENTS
        #             WHERE Graduated = "y"
        #             """, self.docker)['Count'][0]
        #
        # all = pd.read_sql("""SELECT COUNT(*) FROM Students AS "Count" """, self.docker)['Count'][0]
        # graduated_percentage = round((float(graduated)/float(all) * 100), 2)
        # self.scores_df["Percentage of Trainees who Graduate"] = [graduated_percentage]











if __name__ == '__main__':
    t = AppData()
    t.set_chosen_course('test_21')
    t.set_chosen_student('John Smith')
    t.get_avg_psy_pres_scores_df()
    t.get_successful_applicants()
    t.get_course_table()
    t.get_combo_table()










