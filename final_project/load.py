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

