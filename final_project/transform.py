#!!!!!CHECK INDECIES WITH NEW DATAFRAMES!!!!!
#Tests need refactoring to account for new columns


import pandas as pd

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
    def __init__(self):
        #This is a temporary filepath, will inheret filepath
        self.academy_df = pd.read_csv("C:/Users/willi/Downloads/Business_20_2019-02-11.csv")
        #super().__init__()
        if __name__ == '__main__':
            self.add_columns()
            self.active_nulls()
            self.null_rename()
            self.floats_to_ints()
            print(self.academy_df.to_string())



    def add_columns(self):
        #Create a new column for the Spartan's status, initially populated with Y values
        row_list = []
        for i in range(self.academy_df.index.values[-1] + 1):
            row_list.append("Y")
        self.academy_df.insert(2, "Active", row_list, True)
        #if the candidate is not present the in final week they have dropped off the course and are inactive

    def active_nulls(self):
        #Null values are replaced with 99, an obviously false value
        self.academy_df.fillna(99, inplace=True)

    def null_rename(self):
        #If there are 99s (hence null values) in the final column, that is a solid indication of someone being dropped
        final_index = self.academy_df.columns[-1]
        self.academy_df.loc[self.academy_df[final_index] == 99, "Active"] = "N"

    def floats_to_ints(self):
        #The characteristic columns all contain a "_W" so they can be found that way
        for column in self.academy_df:
            if "_W" in column:
                self.academy_df[column] = self.academy_df[column].astype(int)


test_case_csv = Transform_csv()

class Transform_json():
    def __init__(self):
        self.talent_df = pd.read_json("C:/Users/willi/Downloads/10383.json")
        #Incomplete


