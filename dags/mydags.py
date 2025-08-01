from airflow import DAG
from airflow.operators.python import PythonOperator 
from airflow.operators.bash import BashOperator 
from datetime import datetime, timedelta
from localtos3 import business_tranfer, scraper_transfer, weblogs_transfer
from runspider import scraper_call
from mysqldatadump import backup_mysql_to_s3


    

default_args = {
    "owner": 'airflow',
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}


with DAG(
    dag_id="scraper",
    default_args=default_args,
    description="Webpage for movie data and scraper",
    start_date=datetime(2025, 7, 29),
    schedule_interval="0 7 * * *",
    catchup=False,
    tags=["webpage_start", "scraper"]
) as web_start_dag:

  

    start_scraper = PythonOperator(
        task_id="run_scraper",
        python_callable=scraper_call
    )

    


with DAG(
    dag_id="localtos3",
    default_args=default_args,
    description="Daily data transfer to S3",
    start_date=datetime(2025, 7, 29),
    schedule_interval="0 23 * * *",
    catchup=False,
    tags=["datatransfer"]
) as localtos3_dag:

    start_transfer_bus = PythonOperator(
        task_id="run_transfer",
        python_callable=business_tranfer
    )
    
    start_transfer_scraper=PythonOperator(
        task_id="scraper_tranfer",
        python_callable=scraper_transfer
    )
    
    start_transfer_web_logs=PythonOperator(
        task_id="weblogs_transfer",
        python_callable=weblogs_transfer
    )
    
    start_transfer_bus>>start_transfer_scraper>>start_transfer_web_logs


with DAG(
    dag_id="weekly_mysql_backup",
    default_args=default_args,
    description="Weekly MySQL data backup to S3",
    start_date=datetime(2025, 7, 31),
    schedule_interval="0 2 * * 0",
    catchup=False,
    tags=["database", "backup"],
) as database_backup:

    start_backup = PythonOperator(
        task_id="mysqldatadump",
        python_callable=backup_mysql_to_s3
    )
