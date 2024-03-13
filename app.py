from flask import Flask
import sqlite3

app = Flask(__name__)
con = sqlite3.connect("database.db")

def readFile(path):
    return open(path).read()

@app.route("/")
def index():
    return readFile("views/index.html")

if __name__ == "__main__":
    app.run(debug=True)