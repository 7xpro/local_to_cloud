from flask import Flask, request, render_template_string
import os
import requests
from dotenv import load_dotenv
import logging
import pymysql
from pymysql import Error
from datetime import datetime

app = Flask(__name__)
load_dotenv(".env")

api_key = os.getenv('OMDB_API_KEY')
user=os.getenv('USER_NAME')
password=os.getenv('USER_PASSWORD')
database=os.getenv('DATABASE_NAME')
host=os.getenv('HOST_NAME')


path=datetime.now().strftime("year=%Y/month=%m/day=%d")
check_path = f'C:/Users/arsha/Desktop/hybrid/database/web_userlogs/{path}/'
if not os.path.exists(check_path):
    os.makedirs(check_path)

logging.basicConfig(
    filename=check_path + '/web_user.log',
    
    level=logging.INFO,
    format='%(asctime)s | IP: %(ip)s | Agent: %(agent)s | Movie: %(movie)s'
    )

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
            <img src="{{ movie_data.Poster }}" alt="Movie Poster" style="width:400px; border-radius:10px;">
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

def store_movie_in_db(movie_data,host,user,password,database):
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if connection:
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO searched_movies (title, year, genre, director,plot,imdb_rating, actors, poster,searched_at)
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s, NOW())
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
        print('test')
        print("MySQL Error:", e)

    finally:
        if connection:
            cursor.close()
            connection.close()


@app.before_request
def log_request_info():
    logging.info(f"Request from {request.remote_addr}: {request.method} {request.url}")

@app.route('/', methods=['GET', 'POST'])
def movie_search():
    movie_data = None
    error = None

    if request.method == 'POST':
        movie_name = request.form['movie_name']
        
        user_ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        logging.info('', extra={
            'ip': user_ip,
            'agent': user_agent,
            'movie': movie_name
        })

        url = f"http://www.omdbapi.com/?t={movie_name.strip().replace(' ', '+')}&apikey={api_key}"
        response = requests.get(url)
        result = response.json()


        if result.get('Response') == 'True':
            movie_data = result
            store_movie_in_db(movie_data,host,user,password,database)

        else:
            error = f"Movie '{movie_name}' not found."

    return render_template_string(movie_page, movie_data=movie_data, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
