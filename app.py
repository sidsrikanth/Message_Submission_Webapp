from flask import Flask, g, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('submit.html')

