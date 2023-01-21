from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pyodbc
app = Flask(__name__)

# Connect to the database

server = "dictionaryserver.database.windows.net"
port = 1433
user = "CloudSA9f4581d3"
password = "Betterbegood99!"
database = "Dictionary"

cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+','+str(port)+';DATABASE='+database+';UID='+user+';PWD='+ password)
cursor = cnxn.cursor()


print("Connection established")

# Create a table to store the questions and answers


# Insert some example questions and answers
cursor.execute("INSERT INTO questions VALUES ('What is the capital of France?', 'Paris')")
cursor.execute("INSERT INTO questions VALUES ('What is the largest planet in our solar system?', 'Jupiter')")

# Commit the changes to the database
cnxn.commit()

# Initialize the user's score
score = 0

# Select a random question from the database
cursor.execute('SELECT * FROM questions')
question, answer = cursor.fetchone()

# Prompt the user for an answer
user_answer = input(question + ' ')

# Check if the user's answer is correct
if user_answer.lower() == answer.lower():
    score += 1
    print('Correct! Your score is now', score)
else:
    print('Incorrect. The correct answer is', answer)

# Close the connection to the database
cnxn.close()

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    # Select a random question from the database
    cursor.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT 1')
    question, answer = cursor