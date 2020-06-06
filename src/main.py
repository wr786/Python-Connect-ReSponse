# author: wr786
from flask import Flask, session, render_template, request, redirect, send_from_directory
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.lexers.python import PythonLexer
import sys
import os
import time
import subprocess
import locale

lexer = get_lexer_by_name("python")
formatter = HtmlFormatter(style="colorful")

app = Flask(__name__)

@app.route("/upload", methods=["POST", "GET"])
def uploadCode():   # 上传代码文件，用来交流分享
    code = request.form["code"]
    timestamp = request.form["timestamp"]
    with open(f'./data/code_{timestamp}.py', "w", encoding="utf-8") as f:
        f.write(code)
    # os.rename(f'./data/code_{timestamp}.txt', f'./data/code_{timestamp}.py')
    return f'code_{timestamp}.py'   # 返回文件名，用来和下载进行交互

@app.route("/download/<filename>", methods=['GET']) # 下载代码
def downloadFile(filename):
    return send_from_directory('./data/', filename, as_attachment=True)

@app.route("/highlight", methods=["POST", "GET"])
def addHighlight(): # 给代码加上高亮，运用pygments
    code = request.form["code"]
    html = highlight(code, lexer, formatter)
    return html

@app.route("/runScript", methods=["POST", "GET"])
def runScript():    # 运行代码
    code = request.form["code"]
    inputData = request.form["inputData"]
    timestamp = request.form["timestamp"]
    code = f"""#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
f_handler = open('./data/in_{timestamp}.log', 'r')
sys.stdin = f_handler
""" + code
    with open(f'./data/in_{timestamp}.log', "w", encoding="utf-8") as f:
        f.write(inputData)
    with open(f'./data/code_{timestamp}.py', "w", encoding="utf-8") as f:
        f.write(code)
    try:
        process = subprocess.run(f'python ./data/code_{timestamp}.py',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=1)
        if process.returncode == 0:
            # "\n".join([line.decode('cp936').encode('utf-8') for line in process.stdout.readlines()])
            return "0" + process.stdout
        else:
            return "1" + process.stderr
    except Exception:
        return "1" + "Unknown Error:\nMaybe you used some illegal character in your code, you can try replacing them.\nOr maybe it's just a TLE.\n"
    finally:
        os.remove(f'./data/in_{timestamp}.log')
        os.remove(f'./data/code_{timestamp}.py')

@app.route("/")
def index() :
    return render_template("index.html")

if __name__ == "__main__":
    print(os.path.abspath("."))
    app.run(port=80, debug=True)