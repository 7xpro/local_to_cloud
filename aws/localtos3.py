import pandas as pd 
import boto3
from io import StringIO
import os 
from dotenv import load_dotenv  
from datetime import datetime
import sys
import json
sys.path.append("C:/Users/arsha/Desktop/Hybrid/scraper/scraper/spiders/")
from categories import get_categories

categori=get_categories()

scraper_file_name =categori.split("/")[-2].split("_")[0]

batch_date=datetime.now().strftime("%Y-%m-%d")

business_file_name="bussiness_data_"+batch_date+".csv"
data_path=f"C:/Users/arsha/Desktop/Hybrid/database/business_data/{business_file_name}"
date_path=datetime.now().strftime("year=%Y/month=%m/day=%d")
business_key_path=date_path+"/business_data.csv"


load_dotenv(".env")

business_bucket = os.getenv('business')
scraper_bucket = os.getenv('scraper')
webuserlog_bucket = os.getenv('webuserlog')


def setup_client(master,data,bucket,path_key):
    
    client = boto3.client(master)
    try:
        client.put_object(
            Bucket=bucket,
            Key=path_key,
            Body=data
        )
        print(f"File uploaded succesfull to {bucket} in {path_key}")
    except Exception as e:
        print(e)
        
        
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


df=pd.read_csv(data_path)
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
#checking if business file is there or not
business_file=check_file('s3', business_bucket, business_key_path)
if not business_file:     
    setup_client('s3',csv_buffer.getvalue(),business_bucket,business_key_path)
else:
    print(f"file already available at {business_bucket} in {business_key_path}")
    
             

#for scraper data transfer  
scraper_file_path="C:/Users/arsha/Desktop/Hybrid/database/scraper/"+date_path+"/"+scraper_file_name+".jl"
#for aws key
scraper_key_path="books/"+date_path+"/"+scraper_file_name+".json"
with open (scraper_file_path,"r") as file:
    json_data=file.read()
scraper_file=check_file("s3",scraper_bucket,scraper_key_path)

if not scraper_file:
    setup_client('s3',json_data,scraper_bucket,scraper_key_path)
else:
    print(f"file already available in {scraper_bucket}/ {scraper_key_path}") 



#web log
web_logs_path="C:/Users/arsha/Desktop/Hybrid/database/web_userlogs/"+date_path+"/web_user.log"
web_log_key_path="logs/"+date_path+"/web_user.log"

web_file=check_file("s3",webuserlog_bucket,web_log_key_path)

if not web_file:
    with open(web_logs_path,"rb") as log_data:
        setup_client("s3",log_data,webuserlog_bucket,web_log_key_path)
else:
    print(f"file already available at {webuserlog_bucket} in {web_log_key_path}")        





  