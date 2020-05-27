# author: wr786
from flask import Flask, session, render_template, request, redirect
import os
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.python import PythonLexer
import time

lexer = get_lexer_by_name("python")
formatter = HtmlFormatter(style="colorful")

app = Flask(__name__)

@app.route("/highlight", methods=["POST", "GET"])
def addHighlight():
    code = request.form["code"]
    html = highlight(code, lexer, formatter)
    return html

@app.route("/runScript", methods=["POST", "GET"])
def runScript():
    code = request.form["code"]
    return "OK"

@app.route("/")
def index() :
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=80, debug=True)