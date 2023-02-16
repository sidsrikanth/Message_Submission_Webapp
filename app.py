from flask import Flask, g, render_template, request, url_for
import sqlite3

app = Flask(__name__)

DB_NAME = 'data/messages.db'
NUM_MESSAGES = 5

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/submit/", methods = ['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template("submit.html")
    else:
        insert_message(request)
        return render_template("submit.html",
                               name = request.form['name'],
                               message = request.form['message'])

@app.route("/view/")
def view():
    messages = random_messages(NUM_MESSAGES)
    return render_template("view.html", messages = messages)

def get_message_db():
    # returns connection to database messages.db which stores users' messages
    # check if database exists in g attribute
    try:
        return g.message_db
    # if not, create database
    except:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            # set id column to store unique auto-incrementing values
            cmd = """CREATE TABLE IF NOT EXISTS messages (
            id INTEGER IDENTITY PRIMARY KEY,
            name TEXT,
            message TEXT);"""
            cur.execute(cmd)
            conn.commit()
            g.message_db = conn
            return g.message_db

def insert_message(request):
    # get connection to messages.db
    conn = get_message_db()
    cur = conn.cursor()

    # get the form data
    name = request.form['name']
    message = request.form['message']

    # insert form data into database
    cur.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
    conn.commit() # ensure row insertion has been saved
    conn.close()

def random_messages(n):
    # get connection to messages.db
    conn = get_message_db()
    cur = conn.cursor()

    # select a random set of a specified number of messages
    cmd = '''SELECT * FROM messages
    ORDER BY RANDOM()
    LIMIT (?)
    '''
    cur.execute(cmd, (n,))
    rows = cur.fetchall()

    # store all names and messages as a list of tuples
    # row[1] corresponds to the name, row[2] to the message
    messages = [(row[1], row[2]) for row in rows]
    conn.close()
    return messages