#from final_project.transform import Transform
from final_project.config import *
import pyodbc
import pandas as pd
import logging


class LoadData:
    def __init__(self, load_choice, df):  # initialisation
        logging.info("----- Initialised LoadData class -----")
        # Code to connect to SQL database, details can be changed in config file
        try:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
                ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
            logging.info("Successfully connected to database")
        except:
            logging.error("Failed to connect to database")

        #Maybe rewritten,
        # initialising the creation of each table
        if load_choice == 'behaviour':
            self.behaviours_list = df
            self.import_behaviours ()
        if load_choice == 'academy':
            self.academy_list = df
            self.import_academy()
        elif load_choice == 'technologies':
            self.technologies = df
            self.import_technologies()
        if load_choice == 'strength':
            self.strength_list = df
            self.import_strengths()
        elif load_choice == 'weakness':
            self.weakness_list = df
            self.import_weaknesses()
        elif load_choice == 'gender':
            self.gender_list = df
            self.import_gender()
        elif load_choice == 'city':
            self.cities_list = df
            self.import_city()
        elif load_choice == 'uni_details':
            self.university_list = df
            self.import_university_details()
        elif load_choice == 'grade':
            self.degree_grade_list = df
            self.import_degree_grade()
        elif load_choice == 'staff_1':
            self.staff_list_1 = df
            self.import_staff()
        elif load_choice == 'staff_2':
            self.staff_list_2 = df
            self.import_staff()
        elif load_choice == 'streams':
            self.streams_list = df
            self.import_stream()
        elif load_choice == 'applicants':
            self.applicants_list = df
            self.import_applicants()
        elif load_choice == 'weekly_results':
            self._list = df
            self.import_()
        elif load_choice == 'courses':
            self.courses_list = df
            self.import_course()
        elif load_choice == 'student':
            self.student_list = df
            self.import_student()
        elif load_choice == 'sparta_day_interview':
            self.sparta_day_interview_list = df
            self.import_sparta_day_interview()
        elif load_choice == 'sparta_day_assessment':
            self.sparta_day_assessment_list = df
            self.import_sparta_day_assessment()


        self.import_strength_junction_table()
        self.import_weakness_junction_table()
        self.import_talent_technologies_junction_table()


    def import_behaviours(self):
        for behaviour in self.behaviours_list:
            check = self.conn.execute("SELECT behaviour_name FROM Behaviours WHERE behaviour_name = ?", behaviour)
            try:
                behaviour == check.fetchone()[0]
            except TypeError:
                self.conn.execute("INSERT INTO behaviours (behaviour_name) VALUES (?), behaviour_name", )
                logging.info(f'The {behaviour} has now been imported')
                self.conn.commit()

    def import_academy(self):
        for academy in self.academy_list:
            check = self.conn.execute('SELECT academy_location FROM Academies WHERE academy_location = ?', academy)
            try:
                academy == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {academy} has now been imported')
                self.conn.execute('INSERT INTO Academies (academy_location) VALUES (?)', academy)
                self.conn.commit()

    def import_technologies(self):
        for tech in self.technologies:
            check = self.conn.execute('SELECT skill_name FROM Technologies WHERE skill_name = ?', tech)
            try:
                tech == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {tech} has now been imported')
                self.conn.execute('INSERT INTO Technologies (skill_name) VALUES (?)', tech)
                self.conn.commit()

    def import_strengths(self):
        for strength in self.strength_list:
            check = self.conn.execute('SELECT strength_name FROM Strengths WHERE strength_name = ?', strength)
            try:
                strength == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {strength} has now been imported')
                self.conn.execute('INSERT INTO Strengths (strength_name) VALUES (?)', strength)
                self.conn.commit()

    def import_weaknesses(self):
        for weakness in self.weakness_list:
            check = self.conn.execute('SELECT weakness_name FROM Weaknesses WHERE weakness_name = ?', weakness)
            try:
                weakness == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {weakness} has now been imported')
                self.conn.execute('INSERT INTO Weaknesses (weakness_name) VALUES (?)', weakness)
                self.conn.commit()

    def import_gender(self):
        for gender in self.gender_list:
            check = self.conn.execute('SELECT gender FROM Gender WHERE gender = ?', gender)
            try:
                gender = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {gender} has now been imported')
                self.conn.execute('INSERT INTO Gender (gender) VALUES (?)', gender)
                self.conn.commit()

    def import_city(self):
        for city in self.cities_list:
            check = self.conn.execute('SELECT city FROM WHERE city = ?', city)
            try:
                city = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {city} has now been imported')
                self.conn.execute('INSERT INTO City (city_name) VALUES (?)', city)
                self.conn.commit()


    def import_university_details(self):
        for university in self.university_list:
            check = self.conn.execute('SELECT university_name FROM University_Details WHERE = ?', university)
            try:
                university = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {university} has now been imported')
                self.conn.execute('INSERT INTO University_Details (university) VALUES (?)', university)
                self.conn.commit()


    def import_degree_grade(self):
        for grade in self.degree_grade_list:
            check = self.conn.execute('SELECT classification FROM Degree_Grade WHERE classification = ?', grade)
            try:
                grade = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {grade} has now been imported')
                self.conn.execute('INSERT INTO Degree_Grade (classification) VALUES (?)', grade)
                self.conn.commit()

    def import_staff(self):
        for staff_1 in self.staff_list_1:
            check = self.conn.execute('SELECT Staff FROM staff_name WHERE staff_name = ?', staff_1)
            try:
                staff_1 = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {staff_1} has now been imported')
                self.conn.execute('INSERT INTO Staff (staff_name) VALUES (?)', staff_1)
                self.conn.commit()

        for staff_2 in self.staff_list_2:
            check = self.conn.execute('SELECT Staff FROM staff_name WHERE staff_name = ?', staff_2)
            try:
                staff_2 = check.fetchone()[0]
                pass
            except TypeError:
                logging.info(f'The {check} has now been imported')
                self.conn.execute('INSERT INTO Staff (staff_name) VALUES (?)', staff_2)
                self.conn.commit()


    def import_stream(self):
        for stream in self.streams_list:
            check = self.conn.execute('SELECT stream_name FROM Streams WHERE = ?', stream)
            try:
                stream = check.fetchone()[0]
            except TypeError:
                logging.info(f'The {stream} has now been imported')
                self.conn.execute('INSERT INTO Streams (stream_name) VALUES (?)', stream)
                self.conn.commit()

    def import_applicants(self):

        for index, row in self.applicants_list:
            get_gender = self.conn.execute("SELECT gender_id FROM Gender WHERE gender = ?", row.gender)
            get_city = self.conn.execute("SELECT city_id FROM City WHERE city_name = ?",  row.city)
            get_uni = self.conn.execute("SELECT university_id FROM University_Details WHERE university_name = ?", row.uni)
            get_grade = self.conn.execute("SELECT degree_grade_id FROM Degree_Grade WHERE classification = ?", row.grade)
            get_staff = self.conn.execute("SELECT staff_id FROM Staff WHERE staff_name = ?", row.name)
            gender_id = get_gender.fetchone()[0]
            city_id = get_city.fetchone()[0]
            uni_id = get_uni.fetchone()[0]
            grade_id = get_grade.fetchone()[0]
            staff_id = get_staff.fetchone()[0]

            self.conn.execute('INSERT INTO Applicants (name, gender_id, dob, email, city_id, address, postcode, phone_number, university_id, degree_grade_id, staff_id ) '
                              'VALUES (?,?,?,?,?,?,?,?,?,?,?)', row.name, gender_id, row.dob , row.email ,city_id, row.address,
                              row.postcode, row.phone_number, uni_id, grade_id, staff_id)
            self.conn.commit()

        # self.conn.execute("SELECT gender_id FROM Gender WHERE gender = ")
        # self.conn.execute("SELECT city_id FROM City WHERE city_name = ")
        # self.conn.execute("SELECT university_id FROM University_Details
        #         # WHERE university_name =  ")
        # self.conn.execute("SELECT degree_grade_id FROM Degree_Grade WHERE classification = " )




    def import_weekly_results(self):
        for something in somewhere:
            try:
                self.conn.execute("SELECT applicant_id, behaviour_id, week_number, score FROM Weekly_Results",)


    def import_course(self):
        for index, row in self.academy_df:
            self.conn.execute("SELECT course_name FROM Course WHERE course_name = ?", self.academy_df.course_name)
            self.conn.execute("INSERT INTO Course (course_name) VALUES (?)", self.academy_df.course_name)

    def import_student(self):
        pass

    def import_sparta_day_interview(self):
        pass


    def import_sparta_day_assessment(self):
        pass

    def import_strength_junction_table(self):
        pass

    def import_weakness_junction_table(self):
        pass

    def import_talent_technologies_junction_table(self):
        pass













