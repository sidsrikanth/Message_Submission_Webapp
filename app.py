from flask import Flask, g, render_template, request, url_for
import sqlite3

app = Flask(__name__)

DB_NAME = 'data/messages.db'

@app.route("/")
def main():
    return render_template('main.html') # replace with main.html
    # create a base.html and make everything extend base.html

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
    messages = random_messages(5)
    return render_template("view.html", messages = messages)

def get_message_db():
    # write some helpful comments here
    # try:
    #     return g.message_db
    # except:
    #     g.message_db = sqlite3.connect("messages.db")
    #     cmd = """CREATE TABLE IF NOT EXISTS messages (
    #     id INTEGER NOT NULL IDENTITY PRIMARY KEY,
    #     handle TEXT,
    #     message TEXT,
    #     );
    #     """
    #     cursor = g.message_db.cursor()
    #     cursor.execute(cmd)
    #     g.message_db.commit()
    #     return g.message_db

    try:
        return g.message_db
    except:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()

            cmd = """CREATE TABLE IF NOT EXISTS messages (
            id INTEGER IDENTITY PRIMARY KEY,
            name TEXT,
            message TEXT);"""
            cur.execute(cmd)
            conn.commit()
            g.message_db = conn
            return g.message_db

def insert_message(request):
    # comments
    conn = get_message_db()
    cur = conn.cursor()
    name = request.form['name']
    message = request.form['message']
    cur.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
    conn.commit()
    conn.close()

def random_messages(n):
    # comments
    conn = get_message_db()
    cur = conn.cursor()
    cmd = '''SELECT * FROM messages
    ORDER BY RANDOM()
    LIMIT (?)
    '''
    cur.execute(cmd, (n,))
    rows = cur.fetchall()
    messages = [(row[1], row[2]) for row in rows]
    conn.close()
    return messages