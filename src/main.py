# author: wr786
from flask import Flask, session, render_template, request, redirect
import os
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.python import PythonLexer
import time
import subprocess

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
    inputData = request.form["inputData"]
    code = """
import sys
f_handler_2 = open('./data/in.log', 'r')
sys.stdin = f_handler_2 
""" + code
    with open('./data/in.log', "w") as f:
        f.write(inputData)
    with open('./data/code.py', "w") as f:
        f.write(code)
    process = subprocess.run('python ./data/code.py',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=1)
    if process.returncode == 0:
        return "0" + process.stdout
    else:
        return "1" + process.stderr

@app.route("/")
def index() :
    return render_template("index.html")

if __name__ == "__main__":
    print(os.path.abspath("."))
    app.run(port=80, debug=True)