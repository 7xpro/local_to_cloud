import subprocess
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(".env")

password = os.getenv('MYSQLPASS')
database_name = os.getenv("DATABASE_NAME")
print(password, database_name)

# Get today's date in folder format
by_date = datetime.now().strftime("year=%Y/month=%m/day=%d")
print(by_date)

# Construct folder and file path
dump_path = f'C:/Users/arsha/Desktop/Hybrid/database/Mysql/{by_date}/'
backup_file = os.path.join(dump_path, "backup.sql")

# Create directory if it doesn't exist
if not os.path.exists(dump_path):
    os.makedirs(dump_path)
    print("Directory created")
else:
    print("Already exists")

def dump_data():
    cmd = ["mysqldump", "-u", "root", f"-p{password}", database_name]

    print("Dumping...")
    try:
        with open(backup_file, "w", encoding="utf-8") as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print(" Database dump successful.")
        else:
            print(" Error occurred during dump:\n", result.stderr)
    except Exception as e:
        print("Exception:", e)

dump_data()
