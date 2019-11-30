# server.py
# handles routes of the tweet analyser
# Author: Alan Berman

from flask import Flask, request, redirect, render_template
from flask import current_app
from ops import *
app = Flask(__name__)
app.config['SECRET_KEY']="yabbadabbado"
# load classifier model on start 
app.classifier = load_classifier()

@app.route("/",methods=("POST","GET"))
def home():
    # if submitting a tweet
    form = TweetForm()
    if form.validate_on_submit():
        return redirect("/result.html")
    return render_template("home.html",form=form)

# Thanks to https://stackoverflow.com/questions/55117243/field-validation-in-wtf-forms-flask-redirect-method
@app.route("/result",methods=("POST","GET"))
def result():
    # Classify tweet, return result
    tweet = request.form['tweet']
    result = classify_tweet(current_app.classifier,[tweet])
    return render_template("/result.html",tweet=tweet, result=result)

if "__name__"=='__main__':
    app.run()