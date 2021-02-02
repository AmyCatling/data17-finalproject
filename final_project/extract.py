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
        self.json_dict_list = []
        self.academy_df = None
        self.talent_df = None
        self.all_data_loader()


    def data_checker(self):
        pass
        # if data in SQL, continue
        # if not in sql, append data to csv_file_names_list and same for json in json_file_names_list

    def all_data_loader(self):
        self.retrieve_json_file_names()
        self.retrieve_csv_file_names()

    def retrieve_csv_file_names(self):
        items_in_bucket = [item['Key'] for item in bucket_contents['Contents']]
        self.csv_file_names_list = fnmatch.filter(items_in_bucket, '*.csv')
        print(f"A total of {len(self.csv_file_names_list)} csv files were found in Amazon S3")
        self.csv_to_df()

    def retrieve_json_file_names(self):
        items_in_bucket = [item['Key'] for item in bucket_contents['Contents']]
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
            self.csv_df_list.append(df)
        self.academy_df = pd.concat(self.csv_df_list)


    def json_to_df(self):
        for file in self.json_file_names_list:
            key = file
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
            file = s3_object['Body']
            jsondict = json.load(file)
            jsondf = pd.DataFrame([jsondict])
            self.json_dict_list.append(jsondf)
        self.talent_df = pd.concat(self.json_dict_list)




instance = Extract()
print(instance.academy_df)
# instance.data_checker()


# pprint(bucket_contents)

