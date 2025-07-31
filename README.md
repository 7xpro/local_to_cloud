# local_to_cloud
this is a combination of on primise database  and cloud  services can say hybrid solution for data  problems

there are three scripts and these script are running inside of docker and airflow:
1. apidata.py:- this is a flask web page were user can search for movies details by its name and the search result showen to wepage and also store serached movie data to local mysql database it also genret some basic user logs about user.
2. runspider.py:- this  python script is used to run scrapy scraler it used subprocess to "scrapy crawl books -o output_path"
3. localtos3.py :- this script is used to tranfer all the searched and scraped data to s3 buckets with airflow every night.
4. mysqldatadump.py:-  this file uses pymysql ,pandas, and boto3 to first get data from data base change it into Database then store the data in the local folder from were it then readed  the boto3 and then uploaded to the s3 bucket it also populate another table for last query run detail from were we can filter new data from last run 




Architecture :



