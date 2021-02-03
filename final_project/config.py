# Connecting to AWS Services for Extract.py:
import boto3
s3_client = boto3.client('s3')
bucket_name = 'data17-final-project'
bucket_contents = s3_client.list_objects_v2(Bucket=bucket_name)
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

server = config['login_credentials']['server']
database = config['login_credentials']['database']
username = config['login_credentials']['username']
password = config['login_credentials']['password']