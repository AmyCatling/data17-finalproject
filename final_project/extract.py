import boto3
import fnmatch


s3_client = boto3.client('s3')
bucket_name = 'data17-final-project'
bucket_contents = s3_client.list_objects_v2(Bucket=bucket_name)

def retrieve_csv_file_names():
    csv_list = []
    items_in_bucket = [item['Key'] for item in bucket_contents['Contents']]
    csv_list = fnmatch.filter(items_in_bucket, '*.csv')
    return csv_list

print(retrieve_csv_file_names())