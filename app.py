from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
con = sqlite3.connect("database.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/inloggen")
def inloggen():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)