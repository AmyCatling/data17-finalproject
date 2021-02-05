import fnmatch
from final_project.config import s3_client, bucket_name, bucket_contents
import pandas as pd
import json
from pprint import pprint
import boto3


class Extract:
    def __init__(self, filechoice, devcounter=False):
        # create empty lists and attributes
        self.bucket_contents = []

        self.academy_csv_file_names_list = []
        self.applicant_csv_file_names_list = []
        self.json_file_names_list = []
        self.txt_file_names_list = []

        self.academy_csv_df_list = []
        self.applicant_csv_df_list = []
        self.json_dict_list = []
        self.sparta_day_df_list = []

        self.academy_df = None
        self.applicant_df = None
        self.talent_df = None
        self.sparta_day_df = None

        self.filechoice = filechoice
        self.devcounter = devcounter

        # call methods
        self.get_bucket_contents()


    # function to retrieve everything from a bucket (>1000 items)
    def get_bucket_contents(self):
        kwargs = {'Bucket': bucket_name}
        while True:
            resp = s3_client.list_objects_v2(**kwargs)
            for obj in resp['Contents']:
                self.bucket_contents.append(obj)
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    # function to call retrieval functions for the specified file type
    def all_data_loader(self):
        if self.filechoice == 'json':
            self.retrieve_json_file_names()

        elif self.filechoice == 'academy_csv':
            self.retrieve_academy_csv_file_names()

        elif self.filechoice == 'applicant_csv':
            self.retrieve_applicant_csv_file_names()

        elif self.filechoice == 'txt':
            self.retrieve_txt_file_names()

        elif self.filechoice == 'all':
            self.retrieve_json_file_names()
            self.retrieve_academy_csv_file_names()
            self.retrieve_applicant_csv_file_names()
            self.retrieve_txt_file_names()

    def retrieve_file_names(self, filechoice, location):
        pass
        # print(type(self.bucket_contents))
        # items_in_bucket = [item['Key'] for item in self.bucket_contents]
        # exec(f"global all_Academy_csv; all_Academy_csv = file for file in fnmatch.filter(items_in_bucket, '{location}/*.{filechoice}')")
        # print(all_Academy_csv)
        # self.academy_csv_to_df()

    # 4 functions to retrieve files of each format
    def retrieve_academy_csv_file_names(self):
        items_in_bucket = [item['Key'] for item in self.bucket_contents]
        all_csv = fnmatch.filter(items_in_bucket, '*.csv')
        applicant_csvs = fnmatch.filter(items_in_bucket, '*Applicants.csv')
        self.academy_csv_file_names_list = [file for file in all_csv if file not in applicant_csvs]
        print(self.academy_csv_file_names_list)
        print(f"A total of {len(self.academy_csv_file_names_list)} Academy csv files were found in Amazon S3")
        
        self.academy_csv_to_df()

    def retrieve_applicant_csv_file_names(self):
        items_in_bucket = [item['Key'] for item in self.bucket_contents]
        self.applicant_csv_file_names_list = fnmatch.filter(items_in_bucket, '*Applicants.csv')
        print(self.applicant_csv_file_names_list)
        print(f"A total of {len(self.applicant_csv_file_names_list)} Applicant csv files were found in Amazon S3")
        self.applicant_csv_to_df()

    def retrieve_json_file_names(self):
        items_in_bucket = [item['Key'] for item in self.bucket_contents]
        self.json_file_names_list = fnmatch.filter(items_in_bucket, '*.json')
        print(self.json_file_names_list)
        print(f"A total of {len(self.json_file_names_list)} json files were found in Amazon S3")
        self.json_to_df()

    def retrieve_txt_file_names(self):
        items_in_bucket = [item['Key'] for item in self.bucket_contents]
        self.txt_file_names_list = fnmatch.filter(items_in_bucket, '*.txt')
        print(f"A total of {len(self.txt_file_names_list)} txt files were found in Amazon S3")
        print(self.txt_file_names_list)
        self.txt_to_df()

    def academy_csv_to_df(self):
        for file in self.academy_csv_file_names_list:
            key = file
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
            file = s3_object['Body']
            df = pd.read_csv(file)
            df.insert(0, 'original_file_name', '')
            df['original_file_name'] = key
            df.insert(1, 'course_name', '')
            df.insert(2, 'date', '')
            if 'Business' in key:
                df['course_name'] = key[slice(8, 19)]
                df['date'] = key[slice(20, 30)]
            elif 'Data' in key:
                df['course_name'] = key[slice(8, 15)]
                df['date'] = key[slice(16, 26)]
            elif 'Engineering' in key:
                df['course_name'] = key[slice(8, 22)]
                df['date'] = key[slice(23, 33)]

            for column in df:
                df[column].fillna(101, inplace=True)  ### REMOVE IF THIS BREAKS ANYTHING
            self.academy_csv_df_list.append(df)
        self.academy_df = pd.concat(self.academy_csv_df_list)


    def applicant_csv_to_df(self):
        for file in self.applicant_csv_file_names_list:
            key = file
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
            file = s3_object['Body']
            df = pd.read_csv(file)
            df.insert(0, 'original_file_name', '')
            df['original_file_name'] = key
            self.applicant_csv_df_list.append(df)
        self.applicant_df = pd.concat(self.applicant_csv_df_list)

    def json_to_df(self):
        count = 0
        for file in self.json_file_names_list:
            key = file
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
            file = s3_object['Body']
            jsondict = json.load(file)
            jsondf = pd.DataFrame([jsondict])
            jsondf.insert(0, 'original_file_name', '')
            jsondf['original_file_name'] = key
            self.json_dict_list.append(jsondf)
            count += 1
            if count > 100:
                break
        self.talent_df = pd.concat(self.json_dict_list)

    def txt_to_df(self):
        for file in self.txt_file_names_list:
            key = file
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
            file = s3_object['Body']
            test_df = pd.read_csv(file, header=None, skiprows=3)
            test_df.columns = ['name', 'presentation']
            test_df[['name', 'psychometrics']] = test_df['name'].str.split
            test_df['original_file_name'] = key
            s3_object2 = s3_client.get_object(Bucket=bucket_name, Key=key)
            file2 = s3_object2['Body'].read().decode('utf-8')
            for line in [file2]:
                date = [line.split('\r\n')][0][0]
                academy = [line.split('\r\n')][0][1]
            test_df['date'] = date
            test_df['academy'] = academy.split()[0]
            test_df = test_df[['original_file_name', 'academy', 'date', 'name', 'psychometrics', 'presentation']]
            self.sparta_day_df_list.append(test_df)
        self.sparta_day_df = pd.concat(self.sparta_day_df_list)

    def create_csv(self):
        self.talent_df.to_csv(r'C:\Users\lucio\PycharmProjects\data17-finalproject\talent.csv', index=False)
        self.academy_df.to_csv(r'C:\Users\lucio\PycharmProjects\data17-finalproject\academy.csv', index=False)


if __name__ == '__main__':
    instance = Extract('txt')
    instance.all_data_loader()
    # print(instance.academy_df)
    # print(instance.talent_df)
    # print(instance.applicant_df)
    print(instance.sparta_day_df.to_string())

