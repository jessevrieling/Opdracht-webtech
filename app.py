from flask import Flask, render_template, request, redirect, session, jsonify
from flask_bcrypt import Bcrypt
import sqlite3
from secrets import token_hex
from bs4 import BeautifulSoup
from email.message import EmailMessage
import smtplib
from datetime import timedelta, datetime

app = Flask(__name__)
app.secret_key = token_hex(16)
hasher = Bcrypt()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", loggedIn = session.get("loggedIn"))

@app.route("/inloggen", methods=["GET", "POST"])
def inloggen():
    if request.method == "GET":
        if session.get("loggedIn") == True:
            return redirect("/mijnboekingen")
        else:
            return render_template("login.html", errorCode="", loggedIn = session.get("loggedIn"))
    elif request.method == "POST":
        con = sqlite3.connect("database.db")
        cursor = con.cursor()

        identifier = request.form.get("identifier")
        plainPassword = request.form.get("password")

        query = f"SELECT password FROM users WHERE name=\"{identifier}\" OR email=\"{identifier}\""
        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            return render_template("login.html", errorCode="Onjuist wachtwoord of e-mail", loggedIn = session.get("loggedIn"))
        else:
            passwordHash = result[0]

            if hasher.check_password_hash(passwordHash, plainPassword):
                query = f"SELECT name, id FROM users WHERE name=\"{identifier}\" OR email=\"{identifier}\""
                cursor.execute(query)
                result = cursor.fetchall()

                userId = result[0][1]
                username = result[0][0]

                session["loggedIn"] = True
                session["username"] = username
                session["userId"] = userId

                print(session.get("userId"))
                con.close()
                return redirect("/")
            else:
                return render_template("login.html", errorCode="Onjuist wachtwoord of e-mail", loggedIn = session.get("loggedIn"))
        
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

@app.route('/disable_dates', methods=["GET"])
def get_disabled_dates():
    disabled_dates = list()
    if session.get("loggedIn"):
        hID = request.args.get('hID', type=int)
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        query = f"SELECT date_arrival, date_departure FROM reservations WHERE houseId = {hID}"
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            disabled_dates.extend(getDateRange(datetime.strptime(row[0], "%Y-%m-%d"), datetime.strptime(row[1], "%Y-%m-%d")))
        con.close()
    return jsonify(disabled_dates)

@app.route("/Gefeliciteerd!", methods=["GET", "POST"])
def aangemeld():
    if request.method == "GET":
        return render_template("aangemeld.html", loggedIn = session.get("loggedIn"))
    elif request.method == "POST":
        return redirect("/")
    
@app.route("/cancel", methods=["POST"])
def cancel():
    if request.method == "POST":

        return boekingen()

@app.route("/mijnboekingen", methods=["GET"])
def boekingen():
    if session.get("loggedIn") == True:
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        query = f"SELECT title, date_arrival, date_departure, houseID FROM reservations JOIN houses ON reservations.houseId = houses.id WHERE userId={session.get("userId")}"
        cursor.execute(query)
        result = cursor.fetchall()
        reservations = list()
        for row in result:
            reservations.append(row)

        query = f"SELECT * FROM houses"
        cursor.execute(query)
        result = cursor.fetchall()
        houses = list()
        for row in result:
            houses.append(row)

        con.close()
        return render_template("boeken.html", reservations=reservations, houses=houses, loggedIn = session.get("loggedIn"))
    else:
        return redirect("/inloggen")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", loggedIn = session.get("loggedIn"))
    elif request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Moet veranderd worden zodat het naar een fatsoenlijke email stuurt but you get the gist
        # Is netter om de emails en wachtwoord te lezen via een JSON voor aanpasbaarheid en security maar is te veel moeite je weet wel
        # Authentication is en blijft kut
        msg = EmailMessage()
        msg['Subject'] = f'Message from {name}'
        msg['From'] = 'parkzeeenduin@gmail.com'
        # msg['To'] = 'bob.bb.bobberton@gmail.com'
        recipients = ['bob.bb.bobberton@gmail.com', 'jessevrieling@gmail.com', 'ruardijtom@gmail.com']
        msg['To'] = ', '.join(recipients)
        msg.set_content(f'Name: {name}\nE-mail: {email}\n\nMessage: {message}')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('parkzeeenduin@gmail.com', 'radw mcuy mfsx xuxs')
            server.send_message(msg)
            server.quit()
        print('successfully sent the mail.')
    return render_template("index.html", loggedIn = session.get("loggedIn"))

@app.route("/uitloggen", methods=["GET"])
def uitloggen():
    session.clear()
    return render_template("uitloggen.html")

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

    return render_template("huisjes.html", houses=houses, loggedIn = session.get("loggedIn"))

@app.route("/wachtwoord_vergeten")
def wachtwoord():
    return render_template("wachtwoord.html", loggedIn = session.get("loggedIn"))

@app.route("/boeking", methods=["GET", "POST"])
def boeking():
    if request.method == "GET":
        if session.get("loggedIn") == True:
            return render_template("boekscherm.html", loggedIn = session.get("loggedIn"))
        else:
            return redirect("/inloggen")
    if request.method == "POST":
        arrival = request.form.get("arrival-date")
        departure = request.form.get("departure-date")
        uID = session.get("userId")
        hID = request.form.get("id")
        comments = request.form.get("comments")
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        query = f"INSERT INTO reservations (date_arrival, date_departure, userID, houseID, text) VALUES(\"{arrival}\", \"{departure}\", \"{uID}\", \"{hID}\",\"{comments}\")"
        cursor.execute(query)
        con.commit()
        con.close()
        return redirect("/Gefeliciteerd!")
    
def getDateRange(start_date, end_date):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates

if __name__ == "__main__":
    app.run(debug=True)