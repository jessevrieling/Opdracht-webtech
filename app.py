from flask import Flask, render_template, request
import sqlite3
import bcrypt

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/inloggen", methods=["GET", "POST"])
def inloggen():
    if request.method == "GET":
        return render_template("login.html")
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

@app.route("/registreren", methods=["GET", "POST"])
def registreren():
    if request.method == "GET":
        return render_template("registreren.html")
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

@app.route("/Gefeliciteerd!", methods=["GET"])
def aangemeld():
    return render_template("aangemeld.html")

@app.route("/mijnboekingen")
def boekingen():
    return render_template("boeken.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/huisjes")
def huisjes():
    return render_template("huisjes.html")

@app.route("/wachtwoord_vergeten")
def wachtwoord():
    return render_template("wachtwoord.html")

if __name__ == "__main__":
    app.run(debug=True)