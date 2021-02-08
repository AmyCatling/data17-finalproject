#from final_project.transform import Transform
from final_project.config import *
import pyodbc
import pandas as pd
import logging


class LoadData:
    def init(self, load_choice, df):  # initialisation
        logging.info("----- Initialised LoadData class -----")
        try:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
                ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
            logging.info("Successfully connected to database")
        except:
            logging.error("Failed to connect to database")

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
        elif load_choice == 'tech':
            self.technologies = df
            self.import_technologies()
        elif load_choice == 'gender':
            self.gender_list = df
            self.import_gender()
        elif load_choice == 'city':
            self.cities_list = df
            self.import_city()
        elif load_choice == 'academy':
            self.academy_list = df
            self.import_academy()
        elif load_choice == 'degree':
            self.degree_grade_list = df
            self.import_degree_grade()
        elif load_choice == 'uni':
            self.university_list = df
            self.import_university_details()

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

    def import_academy(self):
        for academy in self.academy_list:
            check = self.conn.execute('SELECT academy_location FROM Academies WHERE academy_location = ?', academy)
            try:
                academy == check.fetchone()[0]
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

    def import_strengths(self):
        check = self.conn.execute('SELECT strength_name FROM Strengths').fetchall()
        for strength in self.strength_list:
            try:
                if strength in check:
                    pass
            except TypeError:
                logging.info(f'Insert {strength}')
                self.conn.execute('INSERT INTO Strengths (strength_name) VALUES (?)', strength)
            self.conn.commit()

    def import_weaknesses(self):
        for weakness in self.weaknesses:
            check = self.conn.execute('SELECT weakness_name FROM Weaknesses WHERE weakness_name = ?', weakness)
            try:
                weakness == check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} is not in the Weaknesses table. {check} will now be inserted')
                self.conn.execute('INSERT INTO Weaknesses (weakness_name) VALUES (?)', weakness)
            self.conn.commit()


    def import_gender(self):
        for gender in self.gender_list:
            check = self.conn.execute('SELECT gender FROM Gender WHERE gender = ?', gender)
            try:
                gender = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} is not in the Gender table. {check} will now be inserted')
                self.conn.execute('INSERT INTO Gender (gender) VALUES (?)', gender)
            self.conn.commit()


    def import_city(self):
        for city in self.cities_list:
            check = self.conn.execute('SELECT city FROM WHERE city = ?', city)
            try:
                city = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f' The {check} is not in the City table. {check} will now be inserted')
                self.conn.execute('INSERT INTO City (city_name) VALUES (?)', city)
            self.conn.commit()


    def import_university_details(self):
        #I don't know the column name or if I need iterrows plz help
        for university in self.university_list:
            check = self.conn.execute('SELECT university_name FROM University_Details WHERE = ?', university)
            try:
                university = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} is not in the University_Details table. {check} will now be inserted')
                self.conn.execute('INSERT INTO University_Details (university) VALUES (?)', university)
            self.conn.commit()


    def import_degree_grade(self):
        for grade in self.degree_grade_list:
            check = self.conn.execute('SELECT classification FROM Degree_Grade WHERE classification = ?', grade)
            try:
                grade = check.fetchone()[0]
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
        for something in somewhere:
            try:
                self.conn.execute("SELECT applicant_id, behaviour_id, week_number, score FROM Weekly_Results",)

    def import_courses(self):
        for index, row in self.import
        self.conn.execute('INSERT INTO ('course_name', row.)



def import_student(self):
        pass




   def import_sparta_day_interview():
        self.conn








