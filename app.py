from flask import Flask, render_template, request, url_for

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

@app.route("/boeken")
def boekingen():
    return render_template("boeken.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)