from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["get"])
def index():
    return render_template("index.html")

@app.route("/inloggen", methods=["get", "post"])
def inloggen():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)