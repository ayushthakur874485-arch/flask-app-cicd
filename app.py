from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'mysql'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'root'),
        database=os.getenv('MYSQL_DB', 'devops')
    )
    return connection

@app.route('/')
def index():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM messages")
        messages = cursor.fetchall()
        cursor.close()
        connection.close()
    except Exception as e:
        messages = []
        print(f"Error: {e}")
    
    return render_template('index.html', messages=messages)

@app.route('/add_message', methods=['POST'])
def add_message():
    try:
        message = request.form.get('message')
        if message:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO messages (message) VALUES (%s)", (message,))
            connection.commit()
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Error: {e}")
    
    return redirect('/')

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
