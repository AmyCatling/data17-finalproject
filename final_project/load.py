#from final_project.transform import Transform
from final_project.config import *
import pyodbc
import pandas as pd
import logging


class LoadData:
    def init(self, load_choice, df):  # initialisation
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
            ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        # if load_choice == 'talent':
        #     self.talent_df = df
        #     self.import_talent_data()
        # elif load_choice == 'academy':
        #     self.academy_df = df
        #     self.import_academy_data()
        # elif load_choice == 'applicant':
        #     self.applicant_df = df
        #     self.import_applicant_data()
        # elif load_choice == 'sparta_day':
        #     self.sparta_day_df = df
        #     self.import_sparta_day_data()
        if load_choice == 'strength':
            self.strength_list = df
            self.import_strength()
        # if load_choice == 'weakness':
        #     self.weakness_list = df
        #     self.import_weakness()
    def import_course(self):
        for index, row in self.academy_df:
            self.conn.execute("SELECT course_name FROM Course WHERE course_name = ?", self.academy_df.course_name)
            self.conn.execute("INSERT INTO Course (course_name) VALUES (?)", self.academy_df.course_name)

    def import_behaviours(self):
        self.conn.execute("SELECT behaviour_name FROM Behaviours")
        self.conn.execute("INSERT INTO behaviours (behaviour_name) VALUES (?), behaviour_name")

    def import_academies(self):
        for index, row in self.sparta_day_df.iterrows():
            check = self.conn.execute('SELECT academy_location FROM Academies WHERE academy_location = ?', academy)
            try:
                row == check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} is not in the Academies table. {check} will now be inserted')
                self.conn.execute('INSERT INTO Academies (academy_location) VALUES (?)', academy)
            self.conn.commit()

    def import_stream(self):
        self.conn.execute("SELECT course_name FROM Course WHERE stream = ?", self.academy_df.stream)
        self.conn.execute("INSERT INTO Course (course_name) VALUES (?)", self.academy_df.stream)

    def import_technologies(self):
        for tech in self.technologies:
            check = self.conn.execute('SELECT skill_name FROM Technologies WHERE skill_name = ?', tech)
            try:
                tech == check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} is not in the Technologies table. {check} will now be inserted')
                self.conn.execute('INSERT INTO Technologies (skill_name) VALUES (?)', tech)
            self.conn.commit()

    def import_strength(self):
        for strength in self.strength_list:
            check = self.conn.execute('SELECT strength_name FROM Strengths WHERE strength_name = ?', strength)
            try:
                strength == check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} is not the Strengths table. {check} will now be inserted')
                self.conn.execute('INSERT INTO Strengths (strength_name) VALUES (?)', strength)
            self.conn.commit()

    def import_weaknesses(self):
        for weakness in self.weaknesses:
            check = self.conn.execute('SELECT weakness_name FROM Weaknesses WHERE weakness_name = ?', weakness)
            try:
                weakness = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} is not in the Weaknesses table. {check} will now be inserted')
                self.conn.execute('INSERT INTO Weaknesses (weakness_name) VALUES (?)', weakness)
            self.conn.commit()


    def import_gender(self):
        for index, row in self.academy_df.iterrow():
            check = self.conn.execute('SELECT gender FROM Gender WHERE gender = ?', gender)
            try:
                row = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} is not in the Gender table. {check} will now be inserted')
                self.conn.execute('INSERT INTO Gender (gender) VALUES (?)', gender)
            self.conn.commit()


    def import_city(self):
        self.conn.execute("SELECT city_name FROM City")
        self.conn.execute("INSERT INTO City (city_name) VALUES (?)", city)


    def import_university_details(self):
        #I don't know the column name or if I need iterrows plz help
        for university in self.applicant_df['uni']:
            check = self.conn.execute('SELECT university_name FROM University_Details WHERE = ?', university)
            try:
                university = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} is not in the University_Details table. {check} will not be inserted')
                self.conn.execute('INSERT INTO University_Details (university) VALUES (?)', university)
            self.conn.commit()


    def import_degree_grade(self):
        for index, row in self.academy_df.iterrow():
            check = self.conn.execute('SELECT classification FROM Degree_Grade WHERE classification = ?', grade)
            try:
                row = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} is not in the Degree_Grade table. {check} will now be inserted')
                self.conn.execute('INSERT INTO Degree_Grade (classification) VALUES (?)', grade)
            self.conn.commit()



    def import_staff(self):
        for index, row in "SomeRandomMethod":
            try:
                self.conn.execute("SELECT staff_name FROM Staff")
            except:
                self.conn.execute("INSERT INTO Staff (staff_name) VALUES (?)", staff_name)


    def import_applicants(self):
        self.conn.execute('INSERT INTO Applicants (name, gender_id, dob, email, city_id, address, postcode,\
                           phone_number, university_id, degree_grade_id, staff_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                           name, gender_id, dob, email, city_id, address, postcode, phone_number, university_id,
                           degree_grade_id, staff_id)
        self.conn.commit()


    def import_weekly_results(self):
        pass

    def import_courses(self):



   def import_student(self):











