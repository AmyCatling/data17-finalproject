# Import modules
import json
import pandas as pd
import numpy as np
import datetime
from dateutil.parser import parse
from final_project.load import LoadData
import logging


class Transform_academy_csv():
    def __init__(self, academy_df):
        self.academy_df = academy_df
        self.add_columns()
        self.active_nulls()
        self.floats_to_ints()
        self.null_rename()
        self.deactive_nulls()
        logging.info("test logging")
        # self.format_string_tables(academy_df, 'invited_by')
        self.take_column_name()


    def add_columns(self):
        # Create a new column for the Spartan's status, initially populated with Y values
        row_list = []
        for i in range(len(self.academy_df.index.values)):
            row_list.append("Y")
        self.academy_df.insert(4, "Active", row_list, True)
        logging.info("Successfully added active column")

    def active_nulls(self):
        # Null values are replaced with 99, an obviously false value
        for column in self.academy_df:
            if "_W" in column:
                if "_W9" not in column and "_W10" not in column:
                    self.academy_df[column].fillna(99, inplace=True)
                else:
                    self.academy_df[column].fillna(0, inplace=True)

    def null_rename(self):
        # If column equal to 99, removed from course, else trainee graduated
        active_list = []
        for index, row in self.academy_df.iterrows():
            if 99 in row.values:
                active_list.append('N')
            else:
                active_list.append('Y')
        self.academy_df['Active'] = active_list

    def floats_to_ints(self):
        # The characteristic columns all contain a "_W" so they can be found that way
        for column in self.academy_df:
            if "_W" in column:
                self.academy_df[column] = self.academy_df[column].astype(int)

    def deactive_nulls(self):

        self.academy_df = self.academy_df.replace(99, np.nan)
        self.academy_df = self.academy_df.replace(0, np.nan)
        self.academy_df.fillna(0, inplace=True)

    def take_column_name(self):
        print(self.academy_df.columns)
        # self.skills_list = []
        # for i in self.academy_df.columns:
        #     if "_W2" in i:
        #         self.skills_list.append(i[0:-3])
        self.skills_list = [i[0: -3] for i in self.academy_df.columns if "_W2" in i]
        print(self.skills_list)
        f = LoadData('behaviours', self.skills_list)

class Transform_json():
    def __init__(self, talent_df):
        # f = open("C:/Users/joest/Downloads/10383.json")
        # j = json.load(f)
        # self.talent_df = pd.DataFrame([j])
        self.talent_df = talent_df
        self.json_active_bits()
        self.fix_nulls()
        self.date_types_changed()
        self.format_known_tech()
        self.format_stren_weak()
        self.encode_columns()


    def json_active_bits(self):

        relevant_columns = ['self_development', 'geo_flex', 'financial_support_self', 'result']

        for column in relevant_columns:
            column_list = []
            for index, entry in enumerate(self.talent_df[column]):
                if entry == 'Yes' or entry == 'Pass':
                    column_list.append(1)
                elif entry == 'No' or entry == 'Fail':
                    column_list.append(0)
            self.talent_df[column] = column_list

    def fix_nulls(self):
        self.talent_df['tech_self_score'].fillna('None', inplace=True)

    def date_types_changed(self):
        new_dates = []
        for i in self.talent_df['date']:
            if len(i) != 10:
                i = i.replace('//', '/')
            new_dates.append(datetime.datetime.strptime(i, '%d/%m/%Y').date())
        self.talent_df['date'] = new_dates

    def encode_columns(self):

        tech = []
        strengths = []
        weaknesses = []

        for index, row in self.talent_df.iterrows():
            tech.append(str(row.tech_self_score).encode('utf-16'))
            strengths.append(str(row.strengths).encode('utf-8'))
            weaknesses.append(str(row.weaknesses).encode('utf-8'))

        self.talent_df['tech_self_score'] = tech
        self.talent_df['strengths'] = strengths
        self.talent_df['weaknesses'] = weaknesses

    def format_known_tech(self):
        technologies = []
        for index, row in self.talent_df.iterrows():
            # print(type(row.tech_self_score))
            if type(row.tech_self_score) != dict:
                pass
            else:
                for tech in row.tech_self_score.keys():
                    if tech not in technologies:
                        technologies.append(tech)
        f = LoadData('tech', technologies)

    def format_stren_weak(self):
        stren = []
        weak = []
        for index, row in self.talent_df.iterrows():
            # print(type(row.tech_self_score))
            if type(row.strengths) != list:
                pass
            else:
                for s in row.strengths:
                    if s not in stren:
                        stren.append(s)

            if type(row.weaknesses) != list:
                pass
            else:
                for w in row.weaknesses:
                    if w not in weak:
                        weak.append(w)
        f = LoadData('strength', stren)
        g = LoadData('weakness', weak)


class Transform_applicant_csv():

    def __init__(self, applicant_df):
        #self.applicant_df = pd.read_csv("C:/Users/joest/Downloads/April2019Applicants.csv")
        self.applicant_df = applicant_df
        self.drop_id_column()
        self.replace_nan()
        self.fix_applicants_invite_format()
        self.format_phones()
        self.fix_dob_format()
        format_string_tables(applicant_df, 'gender')
        format_string_tables(applicant_df, 'city')
        format_string_tables(applicant_df, 'academy')
        format_string_tables(applicant_df, 'degree')
        format_string_tables(applicant_df, 'uni')


        #print(self.applicant_df.to_string())


    def fix_dob_format(self):
        new_dates = []
        for i in self.applicant_df['dob']:
            if i != 'Unknown':
                if len(i) != 10:
                    i = i.replace('//', '/')
                new_dates.append(datetime.datetime.strptime(i, '%d/%m/%Y').date())
            else:
                new_dates.append(None)

        self.applicant_df['dob'] = new_dates

    def format_phones(self):
        numbers = []
        for number in self.applicant_df['phone_number']:
            if type(number) != float:
                number = number.replace('-', '')
                number = number.replace(' ', '')
                number = number.replace('(', '')
                number = number.replace(')', '')
                numbers.append(number)
            else:
                numbers.append(None)
        self.applicant_df['phone_number'] = numbers

    def fix_applicants_invite_format(self):
        formatted_dates = []
        for index, row in self.applicant_df.iterrows():
            # if row.invited_date is None or type(row.month) == float:
            if row.invited_date == 'Unknown' or row.month == 'Unknown':
                formatted_dates.append(None)
            else:
                datestring = row.month.split(' ')[0]
                datestring += ' '
                datestring += str(int(row.invited_date))
                datestring += ' '
                datestring += row.month.split(' ')[1]
                dt = parse(datestring)
                formatted_dates.append(dt.date())
        self.applicant_df['invited_date'] = formatted_dates
        self.applicant_df.drop('month', axis=1, inplace=True)

    def replace_nan(self):
        self.applicant_df.fillna('Unknown', inplace=True)

    def drop_id_column(self):
        self.applicant_df.drop('id', axis=1, inplace=True)


class Transform_sparta_day_txt():

    def __init__(self, sparta_day_df):
        self.sparta_day_df = sparta_day_df
        self.format_score()
        self.format_date()
        #print(self.sparta_day_df)

    def format_date(self):
        dates = []
        for index,row in self.sparta_day_df.iterrows():

            dates.append(parse(row.date).date())
        self.sparta_day_df['date'] = dates

    def format_score(self):
        ps_score = []
        pr_score = []
        for index, row in self.sparta_day_df.iterrows():
            if row.psychometrics == 'SCRIMGEOUR':
                print('Why the hell is SCRIMGEOUR a result for psychometric testing??')
                ps_score.append(54)
                pr_score.append(int(row.presentation.split(': ')[1].split('/')[0]))
            else:
                ps_score.append(int(row.psychometrics.split(': ')[1].split('/')[0]))
                pr_score.append(int(row.presentation.split(': ')[1].split('/')[0]))
        self.sparta_day_df['psychometrics'] = ps_score
        self.sparta_day_df['presentation'] = pr_score


def format_string_tables(df, column_name):
    # Used for the one column tables, takes a column of a DF, turns into set to remove duplicates
    # then assigns it to a list so it can be iterated through in load
    unique = list(set(df[column_name]))
    f = LoadData(column_name, unique)


if __name__ == '__main__':
    # test = Transform_json()
    # test.talent_df['self_development'] = 'No'
    # print(test.talent_df.to_string())
    # test.json_active_bits()
    # print(test.talent_df.to_string())
    # print(test.talent_df['geo_flex'].dtype)
    # # test.date_types_changed()

    # t = Transform_applicant_csv('df')
    # t.drop_id_column()
    # t.fix_applicants_invite_format()
    # t.format_phones()
    # t.fix_dob_format()
    # t.replace_nan()
    # print(t.applicant_df.to_string())

    # t = Transform_sparta_day_txt(sparta_day)
    # t.format_date()
    # t.format_score()
    # print(t.sparta_day_df.to_string())

    test = Transform_academy_csv(academy_df)