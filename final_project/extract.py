import fnmatch
from final_project.config import s3_client, bucket_name, bucket_contents
import pandas as pd
import json
from pprint import pprint


class Extract:
    def __init__(self):
        self.csv_file_names_list = []
        self.json_file_names_list = []
        self.csv_df_list = []


        self.retrieve_json_file_names()
        self.retrieve_csv_file_names()
        self.academy_df = pd.concat(self.csv_df_list)
        self.talent_df = None



    def retrieve_csv_file_names(self):
        items_in_bucket = [item['Key'] for item in bucket_contents['Contents']]
        self.csv_file_names_list = fnmatch.filter(items_in_bucket, '*.csv')
        print("done")
        self.csv_to_df()

    def retrieve_json_file_names(self):
        items_in_bucket = [item['Key'] for item in bucket_contents['Contents']]
        self.json_file_names_list = fnmatch.filter(items_in_bucket, '*.json')
        self.json_to_df()

    def csv_to_df(self):
        for file in self.csv_file_names_list:
            key = file
            s3_object = s3_client.get_object(
                Bucket=bucket_name,
                Key=key)
            file = s3_object['Body']
            df = pd.read_csv(file)
            self.csv_df_list.append(df)


    def json_to_df(self):
        for file in self.json_file_names_list:
            key = file
            s3_object = s3_client.get_object(
                Bucket=bucket_name,
                Key=key)
            file = s3_object['Body']
            df = json.load(file)
            pprint(df)



instance = Extract()
# print(instance.academy_df)
# print(instance.csv_file_names_list)
# print(instance.csv_df_list)
print(instance.retrieve_json_file_names())
