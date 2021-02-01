#This should probably be a function within a pipeline class, instead of a class in and of itself


import config file
import pyodbc
class Load:

    #initialisaiton variables must be defined
    #If pyodbc variables are not already defined, must be called here
    def __init__(self):
        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + config.server + ';DATABASE=' + config.database + ';UID=' + config.username + ';PWD=' + config.password)
        self.aca_df = academy_dataframe
        self.tal_df = talent_dataframe

    #The current names of columns as well as number is tbd
    def export_academy_data(self):
        for index, row in self.aca_df.itterrows():
            self.conn.execute('INSERT INTO Academy (<columns>)\
                                    VALUES(#number of ? equal to columns'), row.<column names>
        self.conn.commit()



    def export_talent_data(self):
        for index, row in self.tal_df.itterrows():
            self.conn.execute('INSERT INTO Talent (*columns*)\
                                    VALUES(#number of ? equal to columns'), row.<column names>
        self.conn.commit()

    #Once normalised functions will end up with many repeats
    #It would be ideal if this could be avoided, but I don't know how to make the multi-arg arguments

    # Attempt at reducing repeats, probably won't work
    def export_data(self, <multi arg statement for column names>, int for number of columns):
        for index, row in self.df.itterrows():
            self.conn.execute('INSERT INTO <table> (<multi arg column names>)\
                              VALUES(?*int columns and some way to add commas'), row.<multiarg for columns>
        self.conn.commit()