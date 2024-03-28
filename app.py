from flask import Flask, render_template, request, redirect
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

        identifier = request.form.get("identifier")
        plainPassword = request.form.get("password")
        query = f"SELECT password FROM users WHERE name=\"{identifier}\" OR email=\"{identifier}\""

        cursor.execute(query)
        result = cursor.fetchone()
        con.close()
        
        hashedPassword = result[0]

        if bcrypt.checkpw(plainPassword.encode("utf-8"), hashedPassword.encode("utf-8")):
            return "<h1>goed</h1>"
        else:
            return "<h1>fout</h1>"

@app.route("/registreren", methods=["GET", "POST"])
def registreren():
    if request.method == "GET":
        return render_template("registreren.html")
    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        passwordConfirm = request.form.get("passwordConfirm")

        if password == passwordConfirm:
            con = sqlite3.connect("database.db")
            cursor = con.cursor()
        
            bytes = password.encode("utf-8")
            salt = bcrypt.gensalt()
            
            passwordHash = str(bcrypt.hashpw(bytes, salt))

            query = f"INSERT INTO users (email, name, password) VALUES(\"{email}\", \"{name}\", \"{passwordHash}\")"
            cursor.execute(query)
            con.commit()
            con.close()
            return redirect("/Gefeliciteerd!")
        else:
            return "Wachtwoord komt niet overeen"

@app.route("/Gefeliciteerd!", methods=["GET", "POST"])
def aangemeld():
    if request.method == "GET":
        return render_template("aangemeld.html")
    elif request.method == "POST":
        return redirect("/")

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

@app.route("/boeking")
def boeking():
    return render_template("boekscherm.html")

if __name__ == "__main__":
    app.run(debug=True)