# Connecting to AWS Services for Extract.py:
import boto3
import os

s3_client = boto3.client('s3')
bucket_name = 'data17-final-project'
bucket_contents = s3_client.list_objects_v2(Bucket=bucket_name)
import configparser

config = configparser.ConfigParser()
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'config.ini')
config.read(filename)

server = config['login_credentials']['server']
database = config['login_credentials']['database']
username = config['login_credentials']['username']
password = config['login_credentials']['password']