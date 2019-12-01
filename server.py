# API that receives tweets and performs sentiment analysis on them
# Adds these tweets to a Tweets DB. Tweets can also be viewed, either by ID or all at once
# Also, just for fun: a little website where one can submit a tweet and get its sentiment 
# Author: Alan Berman

# Adapted from https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
# and https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

from flask import Flask, request, redirect, render_template, current_app, jsonify, abort
from flask_mysqldb import MySQL
import mysql.connector
from mysql.connector import Error
from ops import *
app = Flask(__name__)
app.config['SECRET_KEY']="yabbadabbado"
# load classifier model on start 
app.classifier = load_classifier()


connection = mysql.connector.connect(host="localhost",database='mysql',user='admin',password='berman',auth_plugin='mysql_native_password')
cursor = connection.cursor()
#cursor = mysql.connection.cursor()
# make Tweets table if not exists
cursor.execute("""CREATE TABLE IF NOT EXISTS Tweets(
id INT AUTO_INCREMENT PRIMARY KEY, author VARCHAR(50) NOT NULL, content VARCHAR(280) NOT NULL,
 sentiment VARCHAR(10) NOT NULL)
""")
cursor.close()

# Just for fun
# Home page where user can submit tweet
# (Doesn't add to a DB)
@app.route("/",methods=("POST","GET"))
def home():
    # if submitting a tweet
    form = TweetForm()
    if form.validate_on_submit():
        return redirect("/result.html")
    return render_template("home.html",form=form)

# Just for fun
# Page redirected to when tweet submitted on home page
# Thanks to https://stackoverflow.com/questions/55117243/field-validation-in-wtf-forms-flask-redirect-method
@app.route("/result",methods=("POST","GET"))
def result():
    # Classify tweet, return result
    tweet = request.form['tweet']
    result = classify_tweet(current_app.classifier,[tweet])
    return render_template("/result.html",tweet=tweet, result=result)

# Gets all tweets in the Tweets database
@app.route("/api/tweets/all", methods=['GET'])
def get_all_tweets():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Tweets")
    result = cursor.fetchall()
    cursor.close()
    return "Tweets:\n\n"+str(result), 200
   
# Gets tweet by its ID in the Tweets databse
# (ID must be known)
@app.route("/api/tweet/<int:tweet_id>", methods=['GET'])
def get_tweet(tweet_id):
    cursor = connection.cursor()
    # Thanks to https://stackoverflow.com/questions/54518722/mysql-connector-could-not-process-parameters
    cursor.execute("SELECT * FROM Tweets WHERE id=%s",(tweet_id,))
    result = cursor.fetchall()
    # if tweet not found in DB, 404
    if cursor.rowcount==0:
        abort(404)
    # else return that row of the Tweets DB
    return str(result),200



# Submits tweet for sentiment analysis
# Also adds tweet to the Tweets DB
# Tweet must be in JSON
# e.g. {"author":"@johnwick","content":"I like puppies"}
@app.route("/api/tweet",methods=["POST"])
def submit_tweet():
    # Return Bad Request if not JSON, or tweet doesn't list an author/have content
    if not request.json or not 'content' in request.json or not 'author' in request.json:
        abort(400)
    # Get sentiment classification of tweet
    # content must in a list otherwise scikit-learn returns an error
    classification = classify_tweet(current_app.classifier,[request.json['content']])
    # Set sentiment according to classification
    if classification == 0:
        sentiment = "Negative"
    else:
        sentiment = "Positive"
    # Add tweet to Tweets DB
    # with the sentiment we got above
    cursor = connection.cursor()
    cursor.execute("""INSERT INTO Tweets(id,author,content,sentiment)
    VALUES (NULL,%s,%s,%s)""",(request.json['author'],request.json['content'],sentiment))
    # Commit to DB
    connection.commit()
    cursor.close()
    # return the sentiment
    return "Tweet's sentiment: "+sentiment, 200

if "__name__"=='__main__':
    app.run()