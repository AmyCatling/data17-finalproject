import fnmatch
from final_project.config import s3_client, bucket_name, bucket_contents, files_list
import pandas as pd
import json
from pprint import pprint
import boto3
import logging


class Extract:
    def __init__(self, filechoice, devcounter=False):
        logging.info(f"------  initialised {__name__} class  ------")
        # call methods
        self.get_bucket_contents()
        self.keys_in_bucket = [item['Key'] for item in self.bucket_contents]
        self.items_in_bucket = []
        self.data_checker()

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


    def data_checker(self):
        self.all_data_extractor()
        #First checks if file_names.csv already exists. If not, it will be created
        if 'file_names.csv' in self.items_in_bucket:
            s3_object = s3_client.get_object(Bucket=bucket_name, Key='file_names.csv')
            self.file_names_df = pd.read_csv(s3_object['Body'])
            print(self.file_names_df['file_name'].values.tolist())
            print(self.academy_df.to_string())

            file_name_lists = [self.applicant_csv_file_names_list, self.json_file_names_list, self.academy_csv_file_names_list, self.txt_file_names_list]
            new_file_names = []

            for list in file_name_lists:
                for name in list:
                    if name not in self.file_names_df["file_name"].values.tolist():
                        new_file_names.append(name)

                    else:
                        self.academy_df = self.academy_df[self.academy_df.original_file_name != name]
                        self.talent_df = self.talent_df[self.talent_df.original_file_name != name]
                        self.sparta_day_df = self.sparta_day_df[self.sparta_day_df.original_file_name != name]
                        self.applicant_df = self.applicant_df[self.applicant_df.original_file_name != name]

                        # df_name_list = [self.academy_df, self.talent_df, self.sparta_day_df, self.applicant_df]
                        # for df in df_name_list:
                        #     index_names = df[df["original_file_name"] != name].index
                        #     df.drop(index_names, inplace=True)
                        #     #df.drop(df[df["original_file_name"] == name].index, inplace=True)
            print(new_file_names)
            df = pd.DataFrame(new_file_names).rename(columns={0: 'file_name'})
            self.file_names_df = pd.concat([df, self.file_names_df])

            # for new_name in new_file_names:
            #     new_name_df = pd.DataFrame(new_name, columns=["file_name"])
            #     self.file_names_df["file_name"].append(new_name_df)
            self.upload_file_names_df()

        # if 'file_names.csv' in self.items_in_bucket:
        #     s3_object = s3_client.get_object(Bucket=bucket_name, Key='file_names.csv')
        #     self.file_names_df = pd.read_csv(s3_object['Body'])
        #     df_name_list = [self.academy_df, self.talent_df, self.sparta_day_df, self.applicant_df]
        #     new_file_names = []
        #
        #     for df_name in df_name_list:
        #         for value in df_name["original_file_name"].values:
        #             if value not in self.file_names_df["file_name"].values:
        #                 new_file_names.append(value)
        #             else:
        #                 index_names = df_name[df_name["file_name"] == value].index
        #                 df_name.drop(index_names, inplace=True)
        #
        #     for new_name in new_file_names:
        #         self.file_names_df["file_name"].append(new_name)
        #     self.upload_file_names_df()

        else:
            file_name_lists = [self.applicant_csv_file_names_list, self.json_file_names_list,
                               self.academy_csv_file_names_list, self.txt_file_names_list]
            for list in file_name_lists:
                for name in list:
                    self.file_names_list.append(name)

            self.file_names_df = pd.DataFrame(self.file_names_list).rename(columns={0: 'file_name'})
            self.upload_file_names_df()

        # else:
        #     self.file_names_df = pd.DataFrame(self.file_names_df, columns=["file_name"])
        #     self.file_names_df['file_name'].append(self.academy_df['original_file_name'])
        #     self.file_names_df['file_name'].append(self.talent_df['original_file_name'])
        #     self.file_names_df['file_name'].append(self.sparta_day_df['original_file_name'])
        #     self.file_names_df['file_name'].append(self.applicant_df['original_file_name'])
        #     self.upload_file_names_df()

    def upload_file_names_df(self):
        #Simple function for pushing file_names.csv into S3
        buffer = io.StringIO()
        self.file_names_df.to_csv(buffer)
        s3_client.put_object(
            Body=buffer.getvalue(),
            Bucket=bucket_name,
            Key='file_names.csv'
        )


    # function to call retrieval functions for the specified file type
    def all_data_extractor(self):
        logging.info(f"Loading data for {self.filechoice} files")

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
        logging.info(f"A total of {len(self.academy_csv_file_names_list)} Academy csv files were found in Amazon S3")

    def retrieve_applicant_csv_file_names(self):
        self.applicant_csv_file_names_list = fnmatch.filter(self.items_in_bucket, '*Applicants.csv')
        logging.info(f"A total of {len(self.applicant_csv_file_names_list)} Applicant csv files were found in Amazon S3")

    def retrieve_json_file_names(self):
        self.json_file_names_list = fnmatch.filter(self.items_in_bucket, '*.json')
        logging.info(f"A total of {len(self.json_file_names_list)} json files were found in Amazon S3")

    def retrieve_txt_file_names(self):
        self.txt_file_names_list = fnmatch.filter(self.items_in_bucket, '*.txt')
        logging.info(f"A total of {len(self.txt_file_names_list)} txt files were found in Amazon S3")

    #4 functions to get files from S3, add columns and convert to dataframes
    def academy_csv_to_df(self):
        for file in self.academy_csv_file_names_list:
            key = file
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=key)
            file = s3_object['Body']
            df = pd.read_csv(file)

            df.insert(0, 'original_file_name', '')
            df.insert(1, 'course_name', '')
            df.insert(2, 'date', '')

            df['original_file_name'] = key
            df['course_name'] = (key.split('/')[1]).rsplit('_', 1)[0]
            df['date'] = ((key.split('/')[1]).rsplit('_', 1)[1]).split('.')[0]

            self.academy_csv_df_list.append(df)
        self.academy_df = pd.concat(self.academy_csv_df_list)
        logging.info("Academy_csv files have been successfully concatenated and are stored in the variable academy_df")
            # .drop_duplicates() Can be used to drop duplicates, can be used in the future


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
        logging.info("Applicant_csv files have been successfully concatenated and are stored in the variable applicant_df")
            # .drop_duplicates() Can be used to drop duplicates, can be used in the future

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
        logging.info("JSON files have been successfully concatenated and are stored in the variable talent_df")
            # .drop_duplicates() Can be used to drop duplicates, can be used in the future

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
                names.append(row['name'].rsplit(' - ', 1)[0]) ###Remove 'r' if this breaks stuff
                psychometric.append(row['name'].rsplit(' - ', 1)[1])
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
        logging.info("Text files have been successfully concatenated and are stored in the variable sparta_day_df")
            # .drop_duplicates() Can be used to drop duplicates, can be used in the future


    def create_csv(self):
        pass
        # self.talent_df.to_csv(r'C:\Users\lucio\PycharmProjects\data17-finalproject\talent.csv', index=False)
        # self.academy_df.to_csv(r'C:\Users\lucio\PycharmProjects\data17-finalproject\academy.csv', index=False)




if __name__ == '__main__':
    instance = Extract('all')
    instance.all_data_extractor()
    # print(instance.applicant_df.to_string())
    print(instance.talent_df.to_string())
    # print(instance.sparta_day_df.to_string())

