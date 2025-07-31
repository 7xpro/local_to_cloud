import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
import boto3
import pymysql


load_dotenv(".env")

mysql_backup_bucket = os.getenv('mysql_backup_bucket')
host = os.getenv('HOST_NAME')
user = os.getenv("USER_NAME")
password =os.getenv("USER_PASSWORD")
database_name = os.getenv("DATABASE_NAME")
port = 3306

# Format today's date for folder path
by_date = datetime.now().strftime("year=%Y/month=%m/day=%d")
mysql_backup_bucket_key = f"{by_date}/backup.csv"

# Local backup path
dump_path = f'/opt/airflow/data/Mysql/{by_date}/'
backup_file = os.path.join(dump_path, "backup.csv")

if not os.path.exists(dump_path):
    os.makedirs(dump_path)
    print("Directory created")
else:
    print("Directory already exists")



def get_conn(backup_file):
    
    
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database_name,
            port=port
        )
        cursor = connection.cursor()

        # Create tracking table
        create_last_run_table = """
        CREATE TABLE IF NOT EXISTS last_run (
            id INT PRIMARY KEY AUTO_INCREMENT,
            query VARCHAR(255),
            run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_last_run_table)

        # Insert this run log
        insert_log = "INSERT INTO last_run (query) VALUES (%s)"
        cursor.execute(insert_log, ("backup",))

        # Get last run time (excluding the just-inserted one)
        get_last_run = "SELECT run_at FROM last_run ORDER BY id DESC LIMIT 1 OFFSET 1"
        cursor.execute(get_last_run)
        last_time_row = cursor.fetchone()

        if last_time_row:
            last_time = last_time_row[0]
        else:
            last_time = "1970-01-01 00:00:00"  # default if first time

        # Fetch new rows
        query = f"SELECT * FROM searched_movies WHERE searched_at > '{last_time}'"
        cursor.execute(query)

        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()

        if result:
            df = pd.DataFrame(result, columns=columns)
            df.to_csv(backup_file, index=False)
            print(" CSV backup created")

            # Upload to S3
            s3 = boto3.client("s3")
            
            try:
                backup_file=s3.head_object(mysql_backup_bucket,mysql_backup_bucket_key)
                print("file already exist")
            except :
                with open(backup_file, "rb") as backupfile:
                    s3.put_object(Bucket=mysql_backup_bucket, Key=mysql_backup_bucket_key, Body=backupfile)
                    print(" Uploaded to S3:", mysql_backup_bucket_key)
                 
        else:
            print("No new rows to back up.")

        connection.commit()

    except Exception as e:
        print(" Error during backup:", e)

    finally:
        cursor.close()
        connection.close()

get_conn(backup_file)
