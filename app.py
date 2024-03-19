from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/inloggen", methods=["GET", "POST"])
def inloggen():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        return render_template("login.html")

@app.route("/registreren", methods=["GET"])
def registreren():
    return render_template("registreren.html")

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