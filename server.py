# server.py
# handles routes of the tweet analyser
# Author: Alan Berman

from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route("/",methods=["POST","GET"])
def home():
    # if submitting a tweet        
    return render_template("home.html")


if "__name__"=='__main__':
    app.run()