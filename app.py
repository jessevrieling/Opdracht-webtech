from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
con = sqlite3.connect("database.db")

@app.route("/", methods=["get"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)