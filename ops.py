# Classifies tweets
from flask_wtf import FlaskForm 
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired
import pickle
from sklearn.naive_bayes import MultinomialNB

# load the stored sklearn classifier
def load_classifier(path='assets/tweet_classifier_model.sav'):
    return pickle.load(open(path,'rb'))

# classify tweet
# 0 = negative tweet, 1 = positive tweet
def classify_tweet(classifier,tweet):
    prediction = classifier.predict(tweet)[0]
    return prediction

# Form to submit tweets for classification
# Thanks to https://hackersandslackers.com/forms-in-flask-wtforms/
class TweetForm(FlaskForm):
    tweet = TextField('Tweet',[DataRequired()])
    submit = SubmitField('Submit Tweet')
