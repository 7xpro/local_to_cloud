import pandas as pd
import os
from datetime import datetime
import boto3
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# Config
mysql_backup_bucket = os.getenv('mysql_backup_bucket')
host = os.getenv('HOST_NAME')
user = os.getenv("USER_NAME")
password = os.getenv("USER_PASSWORD")
database_name = os.getenv("DATABASE_NAME")
port = 3306

# Generate dynamic paths
by_date = datetime.now().strftime("year=%Y/month=%m/day=%d")
mysql_backup_bucket_key = f"{by_date}/backup.csv"
local_folder = f"/opt/airflow/data/Mysql/{by_date}/"
local_file_path = os.path.join(local_folder, "backup.csv")
os.makedirs(local_folder, exist_ok=True)

def backup_mysql_to_s3():

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database_name,
        port=port,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connection.cursor()

    # Create tracking table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS last_run (
            id INT PRIMARY KEY AUTO_INCREMENT,
            query VARCHAR(255),
            run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Get last run time or epoch
    cursor.execute("SELECT run_at FROM last_run ORDER BY id DESC LIMIT 1")
    last_run_result = cursor.fetchone()
    last_run_time = last_run_result['run_at'] if last_run_result else "1970-01-01 00:00:00"

    # Fetch new data
    fetch_query = "SELECT * FROM searched_movies WHERE searched_at > %s"
    cursor.execute(fetch_query, (last_run_time,))
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    if not rows:
        print("No new data to backup.")
        return  #  No failure, just skip
    else:
        df = pd.DataFrame(rows,columns=columns)
        file_exists = os.path.exists(local_file_path)
        df.to_csv(local_file_path, mode='a', index=False, header=not file_exists)
        print(f"save to {local_file_path}")

        # Upload to S3
        with open(local_file_path, "rb") as file_data:
            s3 = boto3.client("s3")
            s3.put_object(Bucket=mysql_backup_bucket, Key=mysql_backup_bucket_key, Body=file_data)

        print("Backup successful. Uploaded:", mysql_backup_bucket_key)

        # Update run log
        cursor.execute("INSERT INTO last_run (query) VALUES (%s)", ("backup",))
        connection.commit()
        cursor.close()
        connection.close()
        

    
backup_mysql_to_s3()        
        
