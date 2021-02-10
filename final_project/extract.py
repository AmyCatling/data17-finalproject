import fnmatch
from final_project.config import s3_client, bucket_name, bucket_contents, files_list
import pandas as pd
import json
from pprint import pprint
import boto3
import logging
import io

#Extract class gets files from S3 and concatenates files of similar formats into Dataframes
class Extract:
    def __init__(self, devcounter=False):
        logging.info(f"------  initialised {__name__} class  ------")

        #get metadata for all files in S3
        self.get_bucket_contents()
        #List of all files in S3 bucket
        self.items_in_bucket = [item['Key'] for item in self.bucket_contents]

        self.check_file_names()
        logging.info("Checked for new files in S3")

        #Create empty dataframes
        self.academy_df = None
        self.applicant_df = None
        self.talent_df = None
        self.sparta_day_df = None

        #Run functions to populate dataframes
        self.applicant_csv_to_df()
        self.academy_csv_to_df()
        self.json_to_df()
        self.txt_to_df()

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

    ###check for new files in S3
    def check_file_names(self):
        #Run a check for if file_names.csv already exists. If it does not, it is created.
        if "file_names.csv" not in self.items_in_bucket:
            logging.info("Creating file: file_names.csv")
            # create file: 'file_names.csv'
            #A list is generated containing all file names in the bucket as well as 'file_name.csv' itself
            self.file_names_list = [file for file in self.items_in_bucket]
            self.file_names_list.append('file_names.csv')
            #The list is used to build a dataframe, containing a single column: file_name
            self.file_names_df = pd.DataFrame(self.file_names_list).rename(columns={0: 'file_name'})
            #The upload function turns it into a csv and pushes to S3
            ###self.upload_file_names_df() ###Un-comment this to create file_names file
            logging.info("Uploaded file: file_names.csv")
            #'file_names.csv' is popped from the list so that it does not unintentionally interfere with csv methods
            self.file_names_list.remove('file_names.csv')


        else:
            logging.info("Getting file names from file_names.csv")
            #If 'file_names.csv' does exist in S3 it will be downloaded
            #The csv will be turned back into a dataframe and then values extracted into a list of old file names
            s3_object = s3_client.get_object(Bucket=bucket_name, Key='file_names.csv')
            self.file_names_df = pd.read_csv(s3_object['Body'])
            old_files = self.file_names_df['file_name'].values.tolist()
            #self.file_names_list is then altered to remove all old file names, so they will not be retrieved from S3
            self.file_names_list = [i for i in self.items_in_bucket if i not in old_files]
            self.file_names_list.append("file_names.csv")

            #A dataframe containing the names of all new files is created
            self.new_files_df = pd.DataFrame(self.file_names_list).rename(columns={0: 'file_name'})
            #The new_files_df is concatenated onto the file_names_df and reassigned
            self.file_names_df = pd.concat([self.file_names_df, self.new_files_df])
            #This new df of all currently used file names is then reuploaded to S3, overwriting the old version
            ###self.upload_file_names_df() ###Un-comment this to create file_names file
            logging.info("updated file: file_names.csv")
            #As before, 'file_names.csv' is popped to not interfere with csv methods
            self.file_names_list.remove('file_names.csv')
        logging.info(f"There are {len(self.file_names_list)} files to extract")

    def upload_file_names_df(self):
        # Simple function for pushing file_names.csv into S3
        buffer = io.StringIO()
        self.file_names_df.to_csv(buffer, index=False)
        s3_client.put_object(
            Body=buffer.getvalue(),
            Bucket=bucket_name,
            Key='file_names.csv'
        )

    #4 functions to get files from S3, add columns and convert to dataframes
    def academy_csv_to_df(self):
        logging.info("Extracting academy csv files")
        self.files_to_extract = [file for file in self.file_names_list if '.csv' in file and 'Academy/' in file]

        for file in self.files_to_extract:
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=file)
            file_obj = s3_object['Body']
            df = pd.read_csv(file_obj)



            df.insert(0, 'original_file_name', file)
            df.insert(1, 'course_name', (file.split('/')[1]).rsplit('_', 1)[0])
            df.insert(2, 'date', ((file.split('/')[1]).rsplit('_', 1)[1]).split('.')[0])

            self.academy_df = pd.concat([df, self.academy_df])
        logging.info("Academy_csv files have been successfully concatenated and are stored in the variable academy_df")


    def applicant_csv_to_df(self):
        logging.info("Extracting applicant csv files")
        self.files_to_extract = [file for file in self.file_names_list if '.csv' in file and 'Talent/' in file]

        for file in self.files_to_extract:
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=file)
            file_obj = s3_object['Body']
            df = pd.read_csv(file_obj)

            df.insert(0, 'original_file_name', file)
            self.applicant_df = pd.concat([df, self.applicant_df])
        logging.info("Applicant_csv files have been successfully concatenated and are stored in the variable applicant_df")

    def json_to_df(self):
        logging.info("Extracting json files")
        self.files_to_extract = [file for file in self.file_names_list if '.json' in file]

        count = 0
        for file in self.files_to_extract:
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=file)
            file_obj = s3_object['Body']
            jsondict = json.load(file_obj)
            jsondf = pd.DataFrame([jsondict])
            jsondf.insert(0, 'original_file_name', file)

            self.talent_df = pd.concat([jsondf, self.talent_df])
            count += 1
            if count > 100:
                break
        logging.info("JSON files have been successfully concatenated and are stored in the variable talent_df")

    def txt_to_df(self):
        logging.info("Extracting text files")
        self.files_to_extract = [file for file in self.file_names_list if '.txt' in file]

        for file in self.files_to_extract:
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=file)
            file_obj = s3_object['Body']
            df = pd.read_csv(file_obj, header=None, skiprows=3)

            df.columns = ['name', 'presentation']

            #Add name, file_name and psychometric columns to dataframe
            names = []
            psychometric = []
            for index, row in df.iterrows():
                names.append(row['name'].rsplit(' - ', 1)[0])
                psychometric.append(row['name'].rsplit(' - ', 1)[1])
            df['name'] = names
            df['psychometrics'] = psychometric
            df['original_file_name'] = file

            # we define s3_object again to now read the skipped rows
            s3_object2 = s3_client.get_object(Bucket=bucket_name, Key=file)
            file_obj2 = s3_object2['Body'].read().decode('utf-8')

            #add date and academy columns to df
            for line in [file_obj2]:
                date = [line.split('\r\n')][0][0]
                academy = [line.split('\r\n')][0][1]
            df['date'] = date
            df['academy'] = academy.split()[0]

            df = df[['original_file_name', 'academy', 'date', 'name', 'psychometrics', 'presentation']]
            
            self.sparta_day_df = pd.concat([df, self.sparta_day_df])
        logging.info("Text files have been successfully concatenated and are stored in the variable sparta_day_df")

if __name__ == '__main__':
    instance = Extract()
    print(type(instance.academy_df))
    print(instance.applicant_df)
    print(instance.talent_df)
    print(instance.sparta_day_df)
