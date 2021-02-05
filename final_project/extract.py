import fnmatch
from final_project.config import s3_client, bucket_name, bucket_contents
import pandas as pd
import json
from pprint import pprint
import boto3


class Extract:
    def __init__(self, filechoice, devcounter=False):
        # call methods
        self.get_bucket_contents()
        self.items_in_bucket = [item['Key'] for item in self.bucket_contents]

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


    # function to retrieve everything from a bucket (>1000 items)
    def get_bucket_contents(self):
        kwargs = {'Bucket': bucket_name}
        self.bucket_contents = []

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
        if self.filechoice == 'all':
            for i in ['json', 'academy_csv', 'applicant_csv', 'txt']:
                exec(f'self.retrieve_{i}_file_names()')
                exec(f'self.{i}_to_df()')
        else:
            exec(f'self.retrieve_{self.filechoice}_file_names()')
            exec(f'self.{self.filechoice}_to_df()')

    # 4 functions to retrieve files of each format
    def retrieve_academy_csv_file_names(self):
        self.academy_csv_file_names_list = [file for file
                                            in fnmatch.filter(self.items_in_bucket, '*.csv')
                                            if file not in fnmatch.filter(self.items_in_bucket, '*Applicants.csv')]
        print(f"A total of {len(self.academy_csv_file_names_list)} Academy csv files were found in Amazon S3")

    def retrieve_applicant_csv_file_names(self):
        self.applicant_csv_file_names_list = fnmatch.filter(self.items_in_bucket, '*Applicants.csv')
        print(f"A total of {len(self.applicant_csv_file_names_list)} Applicant csv files were found in Amazon S3")

    def retrieve_json_file_names(self):
        self.json_file_names_list = fnmatch.filter(self.items_in_bucket, '*.json')
        print(f"A total of {len(self.json_file_names_list)} json files were found in Amazon S3")

    def retrieve_txt_file_names(self):
        self.txt_file_names_list = fnmatch.filter(self.items_in_bucket, '*.txt')
        print(f"A total of {len(self.txt_file_names_list)} txt files were found in Amazon S3")

    #4 functions to get files from S3, add columns and convert to dataframes
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

            # df['course_name'], df['date'] = key.split('_', 1)[0][slice(8)], key.split('_', 1)[1][slice(-4)]
            if 'Business' in file:
                df['course_name'] = file[slice(8, 19)]
                df['date'] = file[slice(20, 30)]
            elif 'Data' in file:
                df['course_name'] = file[slice(8, 15)]
                df['date'] = file[slice(16, 26)]
            elif 'Engineering' in file:
                df['course_name'] = file[slice(8, 22)]
                df['date'] = file[slice(23, 33)]

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
            names = []
            psychometric = []
            for index, row in test_df.iterrows():
                names.append(row['name'].split(' - ')[0])
                psychometric.append(row['name'].split(' - ')[1])
            test_df['name'] = names
            test_df['psychometrics'] = psychometric
            # test_df[['name', 'psychometrics']] = test_df['name'].str.split('-')[0]
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
        pass
        # self.talent_df.to_csv(r'C:\Users\lucio\PycharmProjects\data17-finalproject\talent.csv', index=False)
        # self.academy_df.to_csv(r'C:\Users\lucio\PycharmProjects\data17-finalproject\academy.csv', index=False)


if __name__ == '__main__':
    instance = Extract('academy_csv')
    instance.all_data_loader()
    print(instance.academy_df['course_name'], instance.academy_df['date'])
    print(instance.talent_df)
    print(instance.applicant_df)
    print(instance.sparta_day_df)

