from flask import Flask, request, render_template, send_from_directory
import requests
import pyodbc
import pymongo

# mongodb setup
uri = "mongodb://hackgsu:moqcCeQKiGDZVqYkqchqXtFcDMzxWD3p9MBbIZj2F3GaLaeSAQqu487LW6TCZYLGfuKOFxNl68EKyEmrCGu9fg==@hackgsu.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@hackgsu@"
client = pymongo.MongoClient(uri)
mydb = client["hackgsu"]   
seekers = mydb["seekers"] # seekers consists of job seekers info

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/jd_parser', methods=['GET'])
def home():
    skills = ['machine learning', 'python', 'c++','java','tensorflow','aurdino','keras','deep learning','ios','android','html','css','javascript','aws','azure','powerbi']
    jd = request.form['jd'].lower()

    skills_in_jd = []

    for skill in skills:
        if(skill in jd):
            skills_in_jd.append(skill)
    
    applications = seekers.find()

    table_entries = []
    for application in applications:
        mydict = {}
        score = 0
        candidate_skills = application['skills'].split(',')
        for skill in skills_in_jd:
            if(skill in candidate_skills):
                score += 1
        mydict['score'] = score
        mydict['ph_no'] = application['phone']
        mydict['skills'] = application['skills']
        mydict['education'] = application['education']
        mydict['work_exp'] = application['work_exp']
        table_entries.append(mydict)


    sorted_entries = sorted(table_entries, key = lambda i: i['score'],reverse=True)

    return "sorted_entries"


if __name__ == "__main__":
    app.run(debug=False)


