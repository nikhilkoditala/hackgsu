#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:25:08 2020

@author: nikhil
"""

from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import requests
import json
import pymongo
uri = "mongodb://hackgsu:moqcCeQKiGDZVqYkqchqXtFcDMzxWD3p9MBbIZj2F3GaLaeSAQqu487LW6TCZYLGfuKOFxNl68EKyEmrCGu9fg==@hackgsu.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@hackgsu@"
client = pymongo.MongoClient(uri)
mydb = client["hackgsu"]
users = mydb["users"]

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

api_base = 'https://ec10824514cf.ngrok.io'

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def homepage_submit():
    return redirect(url_for('loginpage'))

@app.route("/login")
def loginpage():
    return render_template('login.html')

@app.route("/student_resume_upload")
def student_resume_upload():
    return render_template('student_resume_upload.html')


@app.route("/student_resume_upload", methods=['POST'])
def student_resume_upload_submit():
    return redirect(url_for('student_profile_form')) 

@app.route("/student_profile_form")
def student_profile_form():
    return render_template('student_profile_form.html')

@app.route("/student_profile_form", methods=['POST','GET'])
def student_profile_form_submit():
    return render_template('student_submitted.html')

@app.route("/login", methods=['POST'])
def loginpage_post():
    username = request.form['username']
    print(username)
    x = users.find_one({"name":username})

    if(x['role'] == 'seeker'):
        return redirect(url_for('student_resume_upload')) 
    else:
        return redirect(url_for('input'))


@app.route("/submit-profile/")
def userprofile():
    return render_template('student_profile_form.html')

@app.route("/formsubmitted/")
def usersubmission():
    return render_template('student_submitted.html')


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
