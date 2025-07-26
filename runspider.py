import datetime
import os
import subprocess
import sys
sys.path.append("C:/Users/arsha/Desktop/Hybrid/scraper/scraper/spiders/")

from categories import get_categories


categori=get_categories()

name =categori.split("/")[-2].split("_")[0]
print(name)



# Build dynamic path
today = datetime.date.today()
output_dir = f"C:/Users/arsha/Desktop/Hybrid/database/scraper/year={today.year}/month={today.month:02}/day={today.day:02}"
output_file = os.path.join(output_dir, name+'.jl')

# Create directory if not exists
os.makedirs(output_dir, exist_ok=True)

project_dir=r"C:/Users/arsha/Desktop/Hybrid/scraper"
os.chdir(project_dir)

subprocess.run(["scrapy", "crawl", "books", "-o", output_file])

