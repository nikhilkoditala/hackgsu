#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 15:25:08 2020

@author: nikhil
"""

from flask import Flask, request, render_template, send_from_directory
import requests

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/login")
def loginpage():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=False)
