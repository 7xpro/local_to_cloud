from flask import Flask, request, render_template_string
import os
import requests
from dotenv import load_dotenv
import logging
import pymysql
from pymysql import Error
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
load_dotenv(".env")

# Environment variables
api_key = os.getenv('OMDB_API_KEY')
user = os.getenv('USER_NAME')
password = os.getenv('USER_PASSWORD')
database = os.getenv('DATABASE_NAME')
host = os.getenv('HOST_NAME')

# Set log file path based on current date
log_dir = Path(f"/app/database/web_userlogs/year={datetime.now().year}/month={datetime.now().month:02}/day={datetime.now().day:02}")
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "web_user.log"

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s | IP: %(ip)s | Agent: %(agent)s | Movie: %(movie)s'
)

# HTML Template
movie_page = '''
<!DOCTYPE html>
<html>
<head>
    <title>Movie Data</title>
      <style>
        body {
            position:relative;
            top:0;
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            position: absolute;
            top: 0;
            bottom: 10;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 10px #ccc;
            text-align: center;
            width: 400px;
        }
        input {
            padding: 10px;
            margin: 10px 0;
            width: 80%;
        }
        button {
            padding: 10px 20px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
        }
        .result {
            margin-top: 20px;
            text-align: left;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Movie Search</h2>
        <form method="post" action="/">
            <input type="text" name="movie_name" placeholder="Enter movie name" required><br>
            <button type="submit">Search</button>
        </form>

        {% if error %}
            <p style="color:red;">{{ error }}</p>
        {% endif %}

        {% if movie_data %}
        <div class="result">
            <h3>{{ movie_data.Title }} ({{ movie_data.Year }})</h3>
            <p><strong>Genre:</strong> {{ movie_data.Genre }}</p>
            <p><strong>Director:</strong> {{ movie_data.Director }}</p>
            <p><strong>Plot:</strong> {{ movie_data.Plot }}</p>
            <p><strong>IMDB Rating:</strong> {{ movie_data.imdbRating }}</p>
            <p><strong>Actors:</strong> {{ movie_data.Actors }}</p>
            <img src="{{ movie_data.Poster }}" alt="Movie Poster">
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

# Function to store movie data in MySQL
def store_movie_in_db(movie_data, host, user, password, database):
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO searched_movies (title, reales_date, genre, director, plot, imdb_rating, actors, poster, searched_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        values = (
            movie_data.get('Title'),
            movie_data.get('Year'),
            movie_data.get('Genre'),
            movie_data.get('Director'),
            movie_data.get('Plot'),
            movie_data.get('imdbRating'),
            movie_data.get('Actors'),
            movie_data.get('Poster')
        )

        cursor.execute(insert_query, values)
        connection.commit()

    except Error as e:
        print("MySQL Error:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/', methods=['GET', 'POST'])
def movie_search():
    movie_data = None
    error = None

    if request.method == 'POST':
        movie_name = request.form['movie_name'].strip()

        user_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')

        # Log request
        logging.info('User search', extra={
            'ip': user_ip,
            'agent': user_agent,
            'movie': movie_name
        })

        url = f"http://www.omdbapi.com/?t={movie_name.replace(' ', '+')}&apikey={api_key}"
        try:
            response = requests.get(url, timeout=5)
            result = response.json()

            if result.get('Response') == 'True':
                movie_data = result
                store_movie_in_db(movie_data, host, user, password, database)
            else:
                error = f"Movie '{movie_name}' not found."
        except Exception as e:
            error = f"Failed to fetch movie data: {str(e)}"

    return render_template_string(movie_page, movie_data=movie_data, error=error)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
