from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import sqlite3
from secrets import token_hex
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = token_hex(16)
hasher = Bcrypt()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/inloggen", methods=["GET", "POST"])
def inloggen():
    if request.method == "GET":
        if session.get("loggedIn") == True:
            return redirect("/mijnboekingen")
        else:
            return render_template("login.html", errorCode="")
    elif request.method == "POST":
        con = sqlite3.connect("database.db")
        cursor = con.cursor()

        identifier = request.form.get("identifier")
        plainPassword = request.form.get("password")

        query = f"SELECT password FROM users WHERE name=\"{identifier}\" OR email=\"{identifier}\""
        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            return render_template("login.html", errorCode="Onjuist wachtwoord of e-mail")
        else:
            passwordHash = result[0]

            if hasher.check_password_hash(passwordHash, plainPassword):
                query = f"SELECT name FROM users WHERE name=\"{identifier}\" OR email=\"{identifier}\""
                cursor.execute(query)
                username = cursor.fetchone()[0]

                session["loggedIn"] = True
                session["username"] = username
                con.close()
                return redirect("/")
            else:
                return render_template("login.html", errorCode="Onjuist wachtwoord of e-mail")
        
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
            query = f"SELECT COUNT(*) FROM users WHERE email=\"{email}\""
            cursor.execute(query)

            if str(cursor.fetchone()[0]) == "0":
                passwordHash = hasher.generate_password_hash(password).decode('utf-8')

                query = f"INSERT INTO users (email, name, password) VALUES(\"{email}\", \"{name}\", \"{passwordHash}\")"
                cursor.execute(query)
                con.commit()
                con.close()
                return redirect("/Gefeliciteerd!")
            else:
                return render_template("registreren.html", errorCode="E-mail al in gebruik")
        else:
            return render_template("registreren.html", errorCode="Wachtwoord komt niet overeen")

@app.route("/Gefeliciteerd!", methods=["GET", "POST"])
def aangemeld():
    if request.method == "GET":
        return render_template("aangemeld.html")
    elif request.method == "POST":
        return redirect("/")

@app.route("/mijnboekingen", methods=["GET"])
def boekingen():
    if session.get("loggedIn") == True:
        return render_template("boeken.html")
    else:
        return redirect("/inloggen")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/huisjes", methods=["GET"])
def huisjes():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    query = "SELECT image_url, title, description, capacity, price, id FROM houses"
    cursor.execute(query)

    result = cursor.fetchall()
    houses = list()

    for row in result:
        houses.append(row)

    return render_template("huisjes.html", houses=houses)

@app.route("/wachtwoord_vergeten")
def wachtwoord():
    return render_template("wachtwoord.html")

@app.route("/boeking", methods=["GET", "POST"])
def boeking():
    if request.method == "GET":
        if session.get("loggedIn") == True:
            return render_template("boekscherm.html")
        else:
            return redirect("/inloggen")
    elif request.method == "POST":

        arrival = request.form.get("arrival-date")
        departure = request.form.get("departure-date")
        uID = session.get("userId")
        hID = request.args.get("id")
        print(hID)

        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        query = f"INSERT INTO reservations (date_arrival, date_departure, userID, houseID) VALUES(\"{arrival}\", \"{departure}\", \"{uID}\", \"{hID}\")"
        cursor.execute(query)
        con.commit()
        con.close()
        return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)

soup = BeautifulSoup(html, 'html.parser')

