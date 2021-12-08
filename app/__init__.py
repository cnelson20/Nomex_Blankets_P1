from flask import Flask, render_template
import urllib3, json

app = Flask(__name__)
http = urllib3.poolManager()

@app.route("/")
def index():
    return "";


if __name__ == "__main__":
    app.debug = True;
    app.run()
