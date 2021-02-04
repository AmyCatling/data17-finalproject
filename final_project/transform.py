#!!!!!CHECK INDECIES WITH NEW DATAFRAMES!!!!!
#Check final dates


import json
import pandas as pd
import numpy as np
import datetime
"""
Variables:
self.csv_file_names_list - a list of the names of csvs we iterate through
self.json_file_names_list - a list of the names of jsons we iterate through
self.csv_df_list - a list of dataframes generated from the csv files
self.json_df_list - a list of dataframes generated from the json files
self.talent_df - a dataframe for a given json
self.academy_df - 

"""

# We will add the additional columns

class Transform_csv():
    def __init__(self, academy_df):
        #This is a temporary filepath, will inheret filepath
        #self.academy_df = pd.read_csv("C:/Users/joest/Downloads/Data_29_2019-03-04.csv")
        self.academy_df = academy_df
        #super().__init__()

        self.add_columns()
        self.active_nulls()
        self.null_rename()
        self.floats_to_ints()
        self.deactive_nulls()



    def add_columns(self):
        #Create a new column for the Spartan's status, initially populated with Y values
        row_list = []
        for i in range(len(self.academy_df.index.values)):
            row_list.append("Y")
        print(len(row_list))
        self.academy_df.insert(4, "Active", row_list, True)
        #if the candidate is not present the in final week they have dropped off the course and are inactive

    def active_nulls(self):
        #Null values are replaced with 99, an obviously false value
        for column in self.academy_df:
            # if "_W" in column:
            #     if "_W9" not in column and "_W10" not in column:
            #         self.academy_df[column].fillna(99, inplace=True)
            self.academy_df[column].fillna(99, inplace=True)

    def null_rename(self):
        #If there are 99s (hence null values) in the final column, that is a solid indication of someone being dropped
        final_index = self.academy_df.columns[-1]
        self.academy_df.loc[self.academy_df[final_index] == 99, "Active"] = "N"

    def floats_to_ints(self):
        #The characteristic columns all contain a "_W" so they can be found that way
        for column in self.academy_df:
            if "_W" in column:
                    self.academy_df[column] = self.academy_df[column].astype(int)

    def deactive_nulls(self):

        self.academy_df = self.academy_df.replace(99, 0)


# test_case_csv = Transform_csv()

class Transform_json():
    def __init__(self, talent_df):
        # f = open("C:/Users/joest/Downloads/10383.json")
        # j = json.load(f)
        # self.talent_df = pd.DataFrame([j])
        self.talent_df = talent_df
        #self.json_active_bits()
        self.fix_nulls()
        #self.date_types_changed()

        # self.json_active_bits()
        # self.date_types_changed()
        # print(self.talent_df.dtypes)
        #Incomplete



    def json_active_bits(self):

        # final_index = self.academy_df.columns[-1]
        # self.academy_df.loc[self.academy_df[final_index] == 99, "Active"] = "N"
        relevant_columns = ['self_development','geo_flex','financial_support_self', 'result']

        # self.talent_df.loc[self.talent_df[relevant_columns] == 'Yes'] = True

        for column in relevant_columns:
            for index, entry in enumerate(self.talent_df[column]):
                #self.talent_df[column].replace({'Yes': True, 'No': False, 'Pass': True, 'Fail': False})
                if entry == 'Yes' or entry == 'Pass':
                    self.talent_df[column][index] = 'True'
                elif entry == 'No' or entry == 'Fail':
                    self.talent_df[column][index] = 'False'
            self.talent_df[column] = self.talent_df[column].astype(bool)  # ignore me

    def fix_nulls(self):
        self.talent_df['tech_self_score'].fillna('None', inplace=True)

    def date_types_changed(self):
        new_dates = []
        for i in self.talent_df['date']:

            new_dates.append(datetime.datetime.strptime(i, '%d/%m/%Y').date())
        print(type(new_dates[0]))


    #iterate through string columns and encode them inplace








if __name__ == '__main__':
    # test = Transform_json()
    # test.talent_df['self_development'] = 'No'
    # print(test.talent_df.to_string())
    # test.json_active_bits()
    # print(test.talent_df.to_string())
    # print(test.talent_df['geo_flex'].dtype)
    # # test.date_types_changed()
    t = Transform_csv()






