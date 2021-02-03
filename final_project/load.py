#from final_project.transform import Transform
import config
import pyodbc
import pandas as pd


class LoadData:

    def __init__(self):  # initialisation
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + config.server +
            ';DATABASE=' + config.database + ';UID=' + config.username + ';PWD=' + config.password)
        #self.talent_df = talent_df
        #self.academy_df = academy_df

        print(self.conn)

    def import_talent_data(self):  # import talent team data
        for index, row in self.talent_df.itterrows():
            self.conn.execute('INSERT INTO Talent(talent_name, assessment_day, known_technologies,\
                              strengths, weaknesses, self_development, geo_flexible, financial_support_self,\
                              result, course_interest) VALUES (?,?,?,?,?,?,?,?,?,?)', row.name, row.date,
                              row.tech_self_socre, row.strengths, row.weaknesses, row.self_development,
                              row.geo_flex, row.financial_support_self, row.result, row.course_intrest)
        self.conn.commit()

    def import_academy_data(self):  # import academy data
        for index, row in self.academy_df.itterrows():  # iterate through academy df

            try:  # get a talent_id from the Talent table
                get_talent_id = self.conn.execute("SELECT talent_id FROM Talent WHERE talent_name = ? ", row.name)
                talent_id = get_talent_id.fetchone()
            except TypeError:
                print("This person was not present at the talent day")

            self.conn.execute('INSERT INTO Academy (trainer,\
                                                analytical_w1,\
                                                independent_w1,\
                                                determined_w1,\
                                                professional_w1,\
                                                studious_w1,\
                                                imaginative_w1,\
                                                analytical_w2,\
                                                independent_w2,\
                                                determined_w2,\
                                                professional_w2,\
                                                studious_w2,\
                                                imaginative_w2,\
                                                analytical_w3,\
                                                independent_w3,\
                                                determined_w3,\
                                                professional_w3,\
                                                studious_w3,\
                                                imaginative_w3,\
                                                analytical_w4,\
                                                independent_w4,\
                                                determined_w4,\
                                                professional_w4,\
                                                studious_w4,\
                                                imaginative_w4,\
                                                analytical_w5,\
                                                independent_w5,\
                                                determined_w5,\
                                                professional_w5,\
                                                studious_w5,\
                                                imaginative_w5,\
                                                analytical_w6,\
                                                independent_w6,\
                                                determined_w6,\
                                                professional_w6,\
                                                studious_w6,\
                                                imaginative_w6,\
                                                analytical_w7,\
                                                independent_w7,\
                                                determined_w7,\
                                                professional_w7,\
                                                studious_w7,\
                                                imaginative_w7,\
                                                analytical_w8,\
                                                independent_w8,\
                                                determined_w8,\
                                                professional_w8,\
                                                studious_w8,\
                                                imaginative_w8,\
                                                analytical_w9,\
                                                independent_w9,\
                                                determined_w9,\
                                                professional_w9,\
                                                studious_w9,\
                                                imaginative_w9,\
                                                analytical_w10,\
                                                independent_w10,\
                                                determined_w10,\
                                                professional_w10,\
                                                studious_w10,\
                                                imaginative_w10,\
                                                course_name,\
                                                active,\
                                                talent_id)\
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', row.trainer, row.Analytic_W1,
                              row.Independent_W1, row.Determined_W1, row.Professional_W1, row.Studious_W1,
                              row.Imginative_W1,
                              row.Analytic_W2, row.Independent_W2, row.Determined_W2, row.Professional_W2,
                              row.Studious_W2, row.Imginative_W2,
                              row.Analytic_W3, row.Independent_W3, row.Determined_W3, row.Professional_W3,
                              row.Studious_W3, row.Imginative_W3,
                              row.Analytic_W4, row.Independent_W4, row.Determined_W4, row.Professional_W4,
                              row.Studious_W4, row.Imginative_W4,
                              row.Analytic_W5, row.Independent_W5, row.Determined_W5, row.Professional_W5,
                              row.Studious_W5, row.Imginative_W5,
                              row.Analytic_W6, row.Independent_W6, row.Determined_W6, row.Professional_W6,
                              row.Studious_W6, row.Imginative_W6,
                              row.Analytic_W7, row.Independent_W7, row.Determined_W7, row.Professional_W7,
                              row.Studious_W7, row.Imginative_W7,
                              row.Analytic_W8, row.Independent_W8, row.Determined_W8, row.Professional_W8,
                              row.Studious_W8, row.Imginative_W8,
                              row.Analytic_W9, row.Independent_W9, row.Determined_W9, row.Professional_W9,
                              row.Studious_W9, row.Imginative_W9,
                              row.Analytic_W10, row.Independent_W10, row.Determined_W10, row.Professional_W10,
                              row.Studious_W10, row.Imginative_W10, row.course_name, row.active, talent_id)
        self.conn.commit()


if __name__ == "__main__":
    load = LoadData()