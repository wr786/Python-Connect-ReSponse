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
import re

# 用于高亮代码
lexer = get_lexer_by_name("python")
formatter = HtmlFormatter(style="colorful")

# 用于记录黑名单
blacklist = []

app = Flask(__name__)

# 用于禁用一些敏感库
def checkBlackList(code):   
    for item in blacklist:
        pattern = re.compile(f'import\s*?{item}')   # 正则表达式防止“留白”
        if re.match(pattern, code) != None:
            return item
    return 'OK'

# 上传代码文件，用来交流分享
@app.route("/upload", methods=["POST", "GET"])
def uploadCode():   
    code = request.form["code"]
    timestamp = request.form["timestamp"]
    with open(f'./data/code_{timestamp}.py', "w", encoding="utf-8") as f:
        f.write(code)
    # os.rename(f'./data/code_{timestamp}.txt', f'./data/code_{timestamp}.py')
    return f'code_{timestamp}.py'   # 返回文件名，用来和下载进行交互

# 下载代码
@app.route("/download/<filename>", methods=['GET']) 
def downloadFile(filename):
    return send_from_directory('./data/', filename, as_attachment=True) # 实现下载文件功能

# 给代码加上高亮，运用pygments
def addHighlight(code): 
    html = highlight(code, lexer, formatter)
    return html

# 分享代码
@app.route("/share/<filename>", methods=['GET']) 
def shareFile(filename):
    code = ""
    with open(f'./data/{filename}', "r", encoding="utf-8") as f:
        code = f.read()
    return render_template(f'shareCode.html', code=addHighlight(code), filename=filename)

# 运行代码
@app.route("/runScript", methods=["POST", "GET"])
def runScript():   
    code = request.form["code"]
    inputData = request.form["inputData"]
    timestamp = request.form["timestamp"]
    cblFlag = checkBlackList(code)  # 判断是否带有黑名单中的库
    if cblFlag != 'OK':
        return "2" + cblFlag
    code = f"""#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
f_handler = open('./data/in_{timestamp}.log', 'r')
sys.stdin = f_handler

""" + code  # 读取输入文件
    with open(f'./data/in_{timestamp}.log', "w", encoding="utf-8") as f:
        f.write(inputData)
    with open(f'./data/code_{timestamp}.py', "w", encoding="utf-8") as f:
        f.write(code)
    try:
        process = subprocess.run(f'python ./data/code_{timestamp}.py',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8",timeout=1)
        if process.returncode == 0: # 正常运行
            # "\n".join([line.decode('cp936').encode('utf-8') for line in process.stdout.readlines()])
            return "0" + process.stdout
        else:   # 出现报错信息
            return "1" + process.stderr
    except Exception:   # 运行失败
        return "1" + "Unknown Error:\nMaybe you used some illegal character in your code, you can try replacing them.\nOr maybe it's just a TLE.\n"
    finally:    # 删除生成的临时代码文件，减少服务器负担
        os.remove(f'./data/in_{timestamp}.log')
        os.remove(f'./data/code_{timestamp}.py')

@app.route("/")
def index() :
    return render_template("index.html")

if __name__ == "__main__":
    if not os.path.exists('./data'):    # 防止因为data文件夹不存在造成的报错
        os.mkdir('data') 
    with open('./blacklist.ini', 'r') as f:
        blacklist = f.read().splitlines()
    app.run(port=80, debug=True)