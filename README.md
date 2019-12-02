# tweet_analyser

A small API that uses a trained ```scikit-learn``` classifier to perform sentiment analysis on tweets. These tweets
are added to a MySQL database 'Tweets'.

A ```scikit-learn MultinomialNB``` classifier trained on the _Sentiment140_ tweets dataset is used to classify
tweets.

Technologies used:

  - ```Flask```
  - ```scikit-learn```
  - ```mysql-connector```
  
To run:
  1. Change MySQL credentials as needed in ```assets/config.py```
  2. ```flask run```  (Note the port given, might be e.g. 8000)
  3. That's it!

API Functions:

1. Post a tweet


Tweets can be posted e.g.:

```curl -i -H "Content-Type: application/json" -X POST -d '{"author":"@jake", "content":"why am I ugly"}' http://localhost:5000/api/tweet```

Tweets must be in JSON format and have an author (e.g. @jake) and content (the tweet itself). If valid, the sentiment ("Positive"/"Negative") of the tweet is returned
and the tweet is added to the 'Tweets' database.


2. View a tweet 


Tweets can be viewed by ID e.g. ```id=13```:

``` curl -i http://localhost:5000/api/tweet/13```

If the tweet is found, the tweet is returned else a 404 is returned

3. View all tweets 

```curl -i http://localhost:5000/api/tweets/all```

All tweets (all records of the Tweets database) are returned

4. View all tweets by an author e.g. ```author=@jake``` 

```curl -i http://localhost:5000/api/tweets/@jake```

If tweet(s) by that author are found, the tweet(s) is/are returned else a 404 is returned

5. View all tweets by sentiment e.g. ```sentiment=positive``` 

```curl -i http://localhost:5000/api/tweets/sentiment/positive```

If tweet(s) of that sentiment are found, the tweet(s) is/are returned else a 404 is returned

6. Delete a tweet

Tweets can be deleted by ID e.g. ```id=12```:

```curl -X DELETE http://localhost:5000/api/tweet/12```

If tweet is found, it is deleted from Tweets.

For fun, one can also navigate to ```http://localhost:5000/``` and submit a tweet. The sentiment of the tweet is then displayed.
Note: Tweets submitted this way are not added to the Tweets database.



