# Classifies tweets

import pickle

# load the stored sklearn classifier
def load_classifier(path='assets/tweet_classifier_model.sav'):
    return pickle.load(open(path,'rb'))

# classify tweet
# 0 = negative tweet, 1 = positive tweet
def classify_tweet(classifier,tweet):
    prediction = classifier.predict(list(tweet))[0]
    return prediction
