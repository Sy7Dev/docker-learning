# app.py

from flask import Flask
import pymysql

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Connect to the MySQL database
    db = pymysql.connect(
        host="db",    # Compose service hostname for MySQL
        user="root",    # Username to connect to MySQL
        password="my-secret-pwd",  # Password for the MySQL user
        database="mysql"      # Name of the database to connect to
    )
    cur = db.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    return f'Hello, World! MySQL version: {version[0]}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)