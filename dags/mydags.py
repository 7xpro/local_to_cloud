from airflow import DAG
from airflow.operators.python import PythonOperator 
from airflow.operators.bash import BashOperator 
from datetime import datetime, timedelta
from localtos3 import business_tranfer, scraper_transfer, weblogs_transfer
from runspider import scraper_call

def run_all_transfar():
    business_tranfer()
    scraper_transfer()
    weblogs_transfer()

default_args = {
    "owner": 'airflow',
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}

# 1️⃣ DAG to start Flask server and run scraper
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

    

# 2️⃣ DAG to transfer local files to S3
with DAG(
    dag_id="localtos3",
    default_args=default_args,
    description="Daily data transfer to S3",
    start_date=datetime(2025, 7, 29),
    schedule_interval="0 23 * * *",
    catchup=False,
    tags=["datatransfer"]
) as localtos3_dag:

    start_transfer = PythonOperator(
        task_id="run_transfer",
        python_callable=run_all_transfar
    )

# 3️⃣ DAG to stop Flask server

