from final_project.config import *
import pyodbc
import pandas as pd
import logging


# Class for loading in the data into the database in SQL
class LoadData:
    def __init__(self, load_choice, df):  # Initialisation
        logging.info("----- Initialised LoadData class -----")
        # Code to connect to SQL database, details can be changed in config file
        try:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
                ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
            logging.info("Successfully connected to database")
        except:
            logging.error("Failed to connect to database")
            raise

        # Maybe rewritten,
        # Initialising the creation of each table
        if load_choice == 'behaviours':
            self.behaviours_list = df
            self.import_behaviours()
        elif load_choice == 'academy':
            self.academy_list = df
            self.import_academy()
        elif load_choice == 'technologies':
            self.technologies_list = df
            self.import_technologies()
        elif load_choice == 'strength':
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
        elif load_choice == 'uni':
            self.university_list = df
            self.import_university_details()
        elif load_choice == 'degree':
            self.degree_grade_list = df
            self.import_degree_grade()
        elif load_choice == 'trainers':
            self.staff_list_1 = df
            self.import_staff_one()
        elif load_choice == 'invited_by':
            self.staff_list_2 = df
            self.import_staff_two()
        elif load_choice == 'academy_df':
            self.academy_df = df
            self.import_stream()
            self.import_weekly_results()
            self.import_student()
        elif load_choice == 'applicant_df':
            self.applicant_df = df
            # print(self.applicant_df.to_string())
            self.import_applicants()
        #elif load_choice == 'academy_df':
        #    self.academy_df = df
        #
        # elif load_choice == 'academy_df':
        #     self.academy_df = df
        #     self.import_courses()
        #elif load_choice == 'academy_df':
        #    self.academy_df = df

        elif load_choice == 'talent_df':
            self.talent_df = df
            self.import_sparta_day_interview()
        elif load_choice == 'sparta_day_df':
            self.sparta_day_df = df
            self.import_sparta_day_assessment()
        elif load_choice == 'talent_df':
            self.talent_df = df
            self.import_sparta_day_interview()
        elif load_choice == 'sparta_day_df':
            self.sparta_day_df = df
            self.import_sparta_day_assessment()

        elif load_choice == 'talent_df':
            self.talent_df = df
            self.import_strength_junction_table()
            self.import_weakness_junction_table()
            self.import_talent_technologies_junction_table()

    # Importing the 6 Sparta Behaviour names into the Behaviours table in the SQL Database
    def import_behaviours(self):
        for behaviour in self.behaviours_list:
            check = self.conn.execute("SELECT behaviour_name FROM Behaviours WHERE behaviour_name = ?", behaviour)
            try:
                behaviour == check.fetchone()[0]
            except TypeError:
                self.conn.execute("INSERT INTO Behaviours (behaviour_name) VALUES (?)", behaviour)
                logging.info(f'The {behaviour} has now been imported')
                self.conn.commit()

    # Importing the Academy locations into the Academies table in the SQL Database
    def import_academy(self):
        for academy in self.academy_list:
            check = self.conn.execute('SELECT academy_location FROM Academies WHERE academy_location = ?', academy)
            try:
                academy == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {academy} has now been imported')
                self.conn.execute('INSERT INTO Academies (academy_location) VALUES (?)', academy)
                self.conn.commit()

    # Importing the technologies skill names into the Technologies table in the SQL Database
    def import_technologies(self):
        for tech in self.technologies_list:
            check = self.conn.execute('SELECT skill_name FROM Technologies WHERE skill_name = ?', tech)
            try:
                tech == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {tech} has now been imported')
                self.conn.execute('INSERT INTO Technologies (skill_name) VALUES (?)', tech)
                self.conn.commit()

    # Importing the strength names into the Strengths table in the SQL Database
    def import_strengths(self):
        for strength in self.strength_list:
            check = self.conn.execute('SELECT strength_name FROM Strengths WHERE strength_name = ?', strength)
            try:
                strength == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {strength} has now been imported')
                self.conn.execute('INSERT INTO Strengths (strength_name) VALUES (?)', strength)
                self.conn.commit()

    # Importing the weakness names into the Weaknesses table in the SQL Database
    def import_weaknesses(self):
        for weakness in self.weakness_list:
            check = self.conn.execute('SELECT weakness_name FROM Weaknesses WHERE weakness_name = ?', weakness)
            try:
                weakness == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {weakness} has now been imported')
                self.conn.execute('INSERT INTO Weaknesses (weakness_name) VALUES (?)', weakness)
                self.conn.commit()

    # Importing the genders into the Gender table in the SQL Database
    def import_gender(self):
        for gender in self.gender_list:
            check = self.conn.execute('SELECT gender FROM Gender WHERE gender = ?', gender)
            try:
                gender == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {gender} has now been imported')
                self.conn.execute('INSERT INTO Gender (gender) VALUES (?)', gender)
                self.conn.commit()

    # Importing the City names into the City table in the SQL Database
    def import_city(self):
        for city in self.cities_list:
            check = self.conn.execute('SELECT city_name FROM City WHERE city_name = ?', city)
            try:
                city == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {city} has now been imported')
                self.conn.execute('INSERT INTO City (city_name) VALUES (?)', city)
                self.conn.commit()

    # Importing the University name into the University_Details table in the SQL Database
    def import_university_details(self):
        for university in self.university_list:
            check = self.conn.execute('SELECT university_name FROM University_Details WHERE university_name = ?',
                                      university)
            try:
                university == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {university} has now been imported')
                self.conn.execute('INSERT INTO University_Details (university_name) VALUES (?)', university)
                self.conn.commit()

    # Importing the Degree classification into the Degree_Grade table in the SQL Database
    def import_degree_grade(self):
        for grade in self.degree_grade_list:
            check = self.conn.execute('SELECT classification FROM Degree_Grade WHERE classification = ?', grade)
            try:
                grade == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {grade} has now been imported')
                self.conn.execute('INSERT INTO Degree_Grade (classification) VALUES (?)', grade)
                self.conn.commit()

    # Importing the Staff names into the Staff table in the SQL Database
    # This is split into staff 1 and staff 2 for the trainers and the recruitment team
    # Together there will be one Sparta Staff table
    def import_staff_one(self):
        for staff_1 in self.staff_list_1:
            check = self.conn.execute('SELECT staff_name FROM Staff WHERE staff_name = ?', staff_1)
            try:
                staff_1 == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {staff_1} has now been imported')
                self.conn.execute('INSERT INTO Staff (staff_name) VALUES (?)', staff_1)
                self.conn.commit()

    # Importing the Staff names into the Staff table in the SQL Database
    def import_staff_two(self):
        for staff_2 in self.staff_list_2:
            check = self.conn.execute('SELECT staff_name FROM Staff WHERE staff_name = ?', staff_2)
            try:
                staff_2 == check.fetchone()[0]
            except TypeError:
                logging.info(f'The {check} has now been imported')
                self.conn.execute('INSERT INTO Staff (staff_name) VALUES (?)', staff_2)
                self.conn.commit()

    # Importing the stream name into the Streams table in the SQL Database
    def import_stream(self):

        final_list =[]
        stream_name_list = list(self.academy_df['course_name'])
        course_start_date_list = list(self.academy_df['course_start_date'])
        course_end_date_list = list(self.academy_df['course_end_date'])
        for index in range(len(course_start_date_list)):
            final_list.append([stream_name_list[index], course_start_date_list[index], course_end_date_list[index]])

        streams = []
        for listie in final_list:
            if listie not in streams:
                streams.append(listie)

        for stream in streams:
            self.conn.execute('INSERT INTO Streams (stream_name, start_date, end_date) VALUES (?,?,?)', stream[0], stream[1], stream[2])
        self.conn.commit()

    # Importing the information about each applicant to Sparta into the Applicants table in the SQL Database
    def import_applicants(self):
        for index, row in self.applicant_df.iterrows():
            get_gender = self.conn.execute("SELECT gender_id FROM Gender WHERE gender = ?", row.gender)
            gender_id = get_gender.fetchone()[0]
            get_city = self.conn.execute("SELECT city_id FROM City WHERE city_name = ?",  row.city)
            city_id = get_city.fetchone()[0]
            get_uni = self.conn.execute("SELECT university_id FROM University_Details WHERE university_name = ?", row.uni)
            uni_id = get_uni.fetchone()[0]
            get_degree = self.conn.execute("SELECT degree_grade_id FROM Degree_Grade WHERE classification = ?", row.degree)
            degree_id = get_degree.fetchone()[0]
            get_staff = self.conn.execute("SELECT staff_id FROM Staff WHERE staff_name = ?", row.invited_by)
            staff_id = get_staff.fetchone()[0]
            self.conn.execute("""INSERT INTO Applicants (name, gender_id, dob, email, city_id, address, postcode_area, phone_number, university_id, degree_grade_id, staff_id )
                              VALUES (?,?,?,?,?,?,?,?,?,?,?)""", row["name"], gender_id, row.dob, row.email, city_id, row.address, row.postcode, row.phone_number, uni_id, degree_id, staff_id)
            self.conn.commit()


    def import_weekly_results(self):
        print('hello')

        behaviours = self.conn.execute("SELECT * FROM Behaviours").fetchall()
        b_names = []
        b_ids = []
        for i in behaviours:
            b_names.append(behaviours[1])
            b_ids.append(behaviours[0])


        for index, row in self.academy_df.iterrows():
            get_applicant_id = self.conn.execute("SELECT applicant_id FROM Applicants WHERE name = ?", row['name'])
            applicant_id = get_applicant_id.fetchone()
            for i in range(len(b_names)):
                for week in range(1,11):
                    score = row[(b_names[i]+ '_W' + str(week))]
                    self.conn.execute("INSERT INTO Weekly_Results (applicant_id, behaviour_id, week_number, score) Values (?,?,?,?)", applicant_id, b_ids[i], week, score)
        self.conn.commit()

    def import_student(self):
        for index, row in self.academy_df.iterrows():
            get_applicant = self.conn.execute("SELECT applicant_id FROM Applicants WHERE name = ?", row["name"])
            applicant_id = get_applicant.fetchone()[0]
            get_stream = self.conn.execute("SELECT stream_id FROM Streams WHERE stream_name = ?", row.course_name)
            stream_id = get_stream.fetchone()[0]
            self.conn.execute("INSERT INTO Student (graduated, applicant_id, stream_id) VALUES (?,?,?)", row.Active, applicant_id, stream_id)
        self.conn.commit()

    def import_sparta_day_interview(self):
        for index, row in self.talent_df.iterrows():
            get_applicant = self.conn.execute("SELECT applicant_id FROM Applicants WHERE name = ?", row["name"])
            applicant_id = get_applicant.fetchone()[0]
            self.conn.execute("""INSERT INTO Sparta_Day_Interview(self_development, geo_flexible, financial_support_self, result, applicant_id)
                              VALUES(?,?,?,?,?)
            """, row.self_development, row.geo_flex, row.financial_support_self, row.result, applicant_id)
        self.conn.commit()

    def import_sparta_day_assessment(self):
        for index, row in self.sparta_day_df.iterrows():
            get_academy = self.conn.execute("SELECT academy_id FROM Academies WHERE academy_location = ?", row.academy)
            academy_id = get_academy.fetchone()[0]
            # get_applicant = self.conn.execute("SELECT applicant_id FROM Applicants WHERE UPPER(name) = ?", row["name"].upper())
            # print(get_applicant.fetchone()[0])
            # applicant_id = get_applicant.fetchone()[0]
            # print(applicant_idself.conn.execute("""INSERT INTO Sparta_Day_Assessment(sparta_day_date, psychometric_score, presentation_score, academy_id, applicant_id)
            #                                 VALUES(?,?,?,?,?)""", row.date, row.psychometrics, row.presentation, academy_id, applicant_id)
            self.conn.execute("""INSERT INTO Sparta_Day_Assessment(sparta_day_date, psychometric_score, presentation_score, academy_id)
                                            VALUES(?,?,?,?)""", row.date, row.psychometrics, row.presentation,academy_id)
        self.conn.commit()

    def import_strength_junction_table(self):
        # for index, row in self.talent_df.iterrows():
        #     get_applicant = self.conn.execute("SELECT applicant_id FROM Applicants WHERE applicant_name = ?",
        #                                       row["name"])
        #     applicant_id = get_applicant.fetchone()[0]
        #     for strength in self.talent_df['strengths']:
        #         get_strength = self.conn.execute("SELECT strength_id FROM Strengths WHERE strength_name = ?", strength)
        #         strength_id = get_strength.fetchone()[0]
        #
        #         self.conn.execute("INSERT INTO Strength_junction_table (applicant_id, strength_id) VALUES (?,?)", applicant_id, strength_id)
        # self.conn.commit()
        for index, row in self.talent_df.iterrows():

            for strength in self.row['strengths']:
                for i in strength:

                    get_strength = self.conn.execute("SELECT strength_id FROM Strengths WHERE strength_name = ?", i)
                    strength_id = get_strength.fetchone()[0]

                    get_applicant = self.conn.execute("SELECT applicant_id FROM Applicants WHERE LOWER(name) = ?",
                                                      row["name"].lower())
                    applicant_id = get_applicant.fetchone()[0]

                    self.conn.execute("INSERT INTO Strength_junction_table (applicant_id, strength_id) VALUES (?,?)",
                                      applicant_id, strength_id)
        self.conn.commit()

    def import_weakness_junction_table(self):
        for index, row in self.talent_df.iterrows():
            get_weakness = self.conn.execute("SELECT weakness_id FROM Weaknesses WHERE weakness_name = ?", row.weakness)
            weakness_id = get_weakness.fetchone()[0]
            get_applicant = self.conn.execute("SELECT applicant_id FROM Applicants WHERE applicant_name = ?", row["name"])
            applicant_id = get_applicant.fetchone()[0]
            self.conn.execute("INSERT INTO Weakness_junction_table( applicant_id, weakness_id ) VALUES (?,?)", applicant_id, weakness_id)
        self.conn.commit()

    def import_talent_technologies_junction_table(self):
        for index, row in self.talent_df.iterrows():
            get_technology = self.conn.execute("SELECT technology_id FROM Technologies WHERE skill_name = ?", row.weakness)
            technology_id = get_technology.fetchone()[0]
            get_applicant = self.conn.execute("SELECT applicant_id FROM Applicants WHERE applicant_name = ?", row["name"])
            applicant_id = get_applicant.fetchone()[0]
            self.conn.execute("INSERT INTO Talent_Technologies_junction( applicant_id, technology_id ) VALUES (?,?)", applicant_id, technology_id)
        self.conn.commit()
