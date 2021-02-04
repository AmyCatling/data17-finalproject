import fnmatch
from final_project.config import s3_client, bucket_name, bucket_contents
import pandas as pd
import json
from pprint import pprint
import boto3


class Extract:
    def __init__(self, filechoice, devcounter=False):
        self.bucket_contents = []
        self.get_bucket_contents()
        self.csv_file_names_list = []
        self.json_file_names_list = []
        self.csv_df_list = []
        self.json_dict_list = []
        self.academy_df = None
        self.talent_df = None
        self.filechoice = filechoice
        self.devcounter = devcounter
        #self.all_data_loader()
        # self.create_csv()

    def data_checker(self):
        pass
        # if data in SQL, continue
        # if not in sql, append data to csv_file_names_list and same for json in json_file_names_list

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

    def all_data_loader(self):
        if self.filechoice == 'json':
            self.retrieve_json_file_names()
        elif self.filechoice == 'csv':
            self.retrieve_csv_file_names()
        elif self.filechoice == 'all':
            self.retrieve_json_file_names()
            self.retrieve_csv_file_names()


    def retrieve_csv_file_names(self):
        items_in_bucket = [item['Key'] for item in self.bucket_contents]
        all_csv = fnmatch.filter(items_in_bucket, '*.csv')
        applicant_csvs = fnmatch.filter(items_in_bucket, '*Applicants.csv')
        self.csv_file_names_list = [file for file in all_csv if file not in applicant_csvs]
        print(self.csv_file_names_list)
        print(f"A total of {len(self.csv_file_names_list)} Academy csv files were found in Amazon S3")
        self.csv_to_df()

    def retrieve_json_file_names(self):
        items_in_bucket = [item['Key'] for item in self.bucket_contents]
        self.json_file_names_list = fnmatch.filter(items_in_bucket, '*.json')
        print(f"A total of {len(self.json_file_names_list)} json files were found in Amazon S3")
        self.json_to_df()

    def csv_to_df(self):
        for file in self.csv_file_names_list:
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
            # for column in df:
            #     df[column].fillna(101, inplace=True) ###REMOVE IF THIS BREAKS ANYTHING
            self.csv_df_list.append(df)
        self.academy_df = pd.concat(self.csv_df_list)

    def json_to_df(self):
        count = 0
        # for file in self.json_file_names_list:
        for file in self.json_file_names_list:
            if self.devcounter and count%10 == 0:
                print(count)
            key = file
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
            file = s3_object['Body']
            jsondict = json.load(file)
            jsondf = pd.DataFrame([jsondict])
            jsondf.insert(0, 'original_file_name', '')
            jsondf['original_file_name'] = key
            self.json_dict_list.append(jsondf)
            count+=1
        self.talent_df = pd.concat(self.json_dict_list)

    def create_csv(self):
        self.talent_df.to_csv(r'C:\Users\lucio\PycharmProjects\data17-finalproject\talent.csv', index=False)
        self.academy_df.to_csv(r'C:\Users\lucio\PycharmProjects\data17-finalproject\academy.csv', index=False)

if __name__ == '__main__':

    instance = Extract()
    instance.all_data_loader()
    print(instance.academy_df.to_string())

# print(instance.academy_df)
# print(instance.talent_df)

# pprint(bucket_contents)
