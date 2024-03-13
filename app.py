from flask import Flask
app = Flask(__name__)

def readFile(path):
    return open(path).read()

@app.route("/")
def index():
    return readFile("views/index.html")

if __name__ == "__main__":
    app.run(debug=True)