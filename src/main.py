# author: wr786
from flask import Flask, session, render_template, request, redirect
import os

app = Flask(__name__)

@app.route("/")
def index() :
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=80, debug=True)