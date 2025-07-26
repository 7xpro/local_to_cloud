import pandas as pd 
import boto3
from io import StringIO
import os 
from dotenv import load_dotenv  
from datetime import datetime


key_path=datetime.now().strftime("year=%Y/month=%m/day=%d/business_data.csv") 

load_dotenv(".env")

business_bucket = os.getenv('business')
scraper_bucket = os.getenv('scraper')
webuserlog_bucket = os.getenv('webuserlog')


def setup_client(master,data,bucket,path_key):
    
    client = boto3.client(master)
    client.put_object(
        Bucket=bucket,
        Key=path_key,
        Body=data
    )

def check_file(master, bucket, path_key):
    client = boto3.client(master)
    try:
        client.head_object(Bucket=bucket, Key=path_key)
        return True
    except client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise e


df=pd.read_csv('database/business_data/salary_data_cleaned.csv')
required_columns = [
    'Job Title',
    'Salary Estimate',
    'Company Name',
    'Location',
    'Industry',
    'avg_salary',
    'python_yn'
]

required_df=df[required_columns]

csv_buffer = StringIO()

required_df.to_csv(csv_buffer, index=False)


business_file=check_file('s3', business_bucket, key_path)

try:
    if not business_file:
        setup_client(
            master='s3',
            data=csv_buffer.getvalue(),
            bucket=business_bucket,
            path_key=key_path
        )
    else:
        print(f"File already exists in {business_bucket} at {key_path}")    
except Exception as e:
    print(f"Error uploading to S3: {e}")    


    



  