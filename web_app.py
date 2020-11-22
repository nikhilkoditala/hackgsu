#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:25:08 2020

@author: nikhil
"""

from flask import Flask, request, render_template, send_from_directory
import requests
import json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

api_base = 'http://825fff06fe98.ngrok.io'

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/login")
def loginpage():
    return render_template('login.html')

@app.route("/jd")
def input():
    return render_template('employer_jd.html')


@app.route("/jd", methods=['POST'])
def form_post(): 
    data = request.form['data'].encode('utf-8')
    data = data.replace(b'\n',b'')
    reply = requests.post(api_base + "/jd_parser", data=data, timeout = 1000).content.decode("utf-8")
    print(reply)
    reply = json.loads(reply)
    scores = [r['score'] for r in reply]
    ph_nos = [r['ph_no'] for r in reply]
    skills = [r['skills'] for r in reply]
    education = [r['education'] for r in reply]
    work_exp = [r['work_exp'] for r in reply]
    return render_template('employer_table.html',mimetype='text/plain' , len = len(scores), scores = scores, ph_nos = ph_nos, skills = skills, education = education, work_exp = work_exp  )
    

if __name__ == "__main__":
    app.run(debug=False, port=5001)
