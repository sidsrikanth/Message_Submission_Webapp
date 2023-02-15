from flask import Flask, g, render_template, request, url_for
import sqlite3

app = Flask(__name__)

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
        return render_template("submit.html")

@app.route("/view/")
def view(): # deleted messages as argument
    messages = random_messages(5)
    return render_template('view.html', messages = messages)

def get_message_db():
  # write some helpful comments here
  try:
    return g.message_db
  except:
    g.message_db = sqlite3.connect("messages_db.sqlite")
    cmd = """CREATE TABLE IF NOT EXISTS messages (
    id INTEGER NOT NULL IDENTITY PRIMARY KEY, 
    handle TEXT,
    message TEXT,
    );
    """
    cursor = g.message_db.cursor()
    cursor.execute(cmd)
    g.message_db.commit()
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
    ORDER BY RAND()
    LIMIT ?
    '''
    cur.execute(cmd, (n,))
    rows = cur.fetchall()
    messages = [(row[1], row[2]) for row in rows]
    conn.close()
    return messages
    