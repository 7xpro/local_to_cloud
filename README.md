# local_to_cloud
this is a combination of on primise database  and cloud  services can say hybrid solution for data  problems




Description:

there are three scripts and these script are running inside of docker and airflow:
1. apidata.py:- this is a flask web page were user can search for movies details by its name and the search result showen to wepage and also store serached movie data to local mysql database it also genret some basic user logs about user.
2. runspider.py:- this  python script is used to run scrapy scraler it used subprocess to "scrapy crawl books -o output_path"
3. localtos3.py :- this script is used to tranfer all the searched and scraped data to s3 buckets with airflow every night.
4. mysqldatadump.py:-  this file uses pymysql ,pandas, and boto3 to first get data from data base change it into Database then store the data in the local folder from were it then readed  the boto3 and then uploaded to the s3 bucket it also populate another table for last query run detail from were we can filter new data from last run 




Architecture :

<img width="911" height="641" alt="final_local_to_s3 drawio" src="https://github.com/user-attachments/assets/ae069cbd-476f-4708-bdbf-041c84b67cbf" />



TechStack:

      - Python
      - Flask
      - MySQL
      - AWS S3, Lambda, Glue, Athena
      - Airflow (for orchestration)
      - docker


📊 Features

- Real-time ingestion of user search data into mysql database(local)
- scrapy for product details
- ETL job to transform and store structured data to  S3
- Schema detection using AWS Glue Crawlers
- SQL analysis using Athena


🚀 How to Run the Project
Step-by-step guide to run it locally or in the cloud

    1. Clone the repo
    2. Set up `.env` file
    3. Build docker container using : docker-compose build
    4. now run the contianer using : docker-compose up

📂 Project Structure  

    HYBRID/
      ├── .vscode/               # VSCode settings (optional, usually ignored)
      ├── dags/                  # Apache Airflow DAGs for orchestration
      ├── database/              # SQL scripts or database-related utilities
      ├── localtocloud/          # Scripts to transfer local data to cloud (e.g., S3)
      ├── scraper/               # Web scraping logic for data extraction
      ├── .env                   # Environment variables (not committed to Git)
      ├── .gitignore             # Git ignored files/folders
      ├── apidata.py             # Script to fetch data from an external API
      ├── docker-compose.yml     # Docker Compose file for multi-container setup
      ├── Dockerfile             # Dockerfile for building the main app container
      ├── README.md              # Project documentation
      ├── requirements.txt       # Python dependencies


Demo:



 Author:
   Arshad khan looking data  relaited job  contact me :- https://www.linkedin.com/in/arshad-khan-a702a9222/
          


