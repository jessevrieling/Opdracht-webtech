import sqlite3
import bcrypt
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("pages/index.html")

@app.route("/inloggen", methods=["GET", "POST"])
def inloggen():
    if request.method == "GET":
        return render_template("pages/login.html")
    elif request.method == "POST":
        con = sqlite3.connect("database.db")
        cursor = con.cursor()

        name = request.form.get("username")
        password = request.form.get("password")
        
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        passwordHash = bcrypt.hashpw(bytes, salt)
        query = f"SELECT COUNT(*) FROM users WHERE name=\"{name}\" AND password=\"{passwordHash}\""
        cursor.execute(query)
        result = cursor.fetchone()

        if result[0] == 1:
            return "<h1>Goed</h1"
        else:
            return "<h1>Fout</h1>"

@app.route("/registreren", methods=["GET"])
def registreren():
    return render_template("pages/registreren.html")

@app.route("/Gefeliciteerd!", methods=["GET"])
def aangemeld():
    return render_template("pages/aangemeld.html")

@app.route("/mijnboekingen")
def boekingen():
    return render_template("pages/boeken.html")

@app.route("/contact")
def contact():
    return render_template("pages/contact.html")

if __name__ == "__main__":
    app.run(debug=True)