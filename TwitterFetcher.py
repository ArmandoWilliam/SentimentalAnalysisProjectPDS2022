from textblob import TextBlob
import tweepy
from tweepy import OAuthHandler
import pandas as pd
from textblob import TextBlob
import re
#import mysql.connector
#from mysql.connector import Error

# Authentication
consumerKey = ''
consumerSecret = ''
accessToken = ''
accessTokenSecret = ''
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


def clean_tweet(tweet):
    return ''.join(re.sub(r"(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)|(http\S+)|(www.\S+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)", " ", tweet))

def get_tweet_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def join_hstg(hstg):
    return ' '.join(hstg)

fetch_tweets = []
players = ['Nadal','Tsitsipas','Djokovic']
limit=1000
for player in players :
    tweets = tweepy.Cursor(api.search_tweets, q=player+'-filter:retweets', count=100, tweet_mode='extended',lang="en").items(limit)

    for tweet in tweets:
        # find the hashtags in the tweet
        hstgs = []
        for hstg in tweet.entities['hashtags']:
            hstgs.append(hstg['text'])

        tweet_dict = {'searchParam': player,
            'user_name': tweet.user.screen_name,
            'text': clean_tweet(tweet.full_text),
            'hashtags': join_hstg(hstgs),
            'date': tweet.created_at,
            'location': tweet.user.location,
            'number_of_followers':tweet.user.followers_count,
            'number_of tweets':tweet.user.statuses_count,
            'sentiment':get_tweet_sentiment(tweet.full_text)
            }

        fetch_tweets.append(tweet_dict)


df_tweets = pd.DataFrame(fetch_tweets)
print(df_tweets)


#try:
    #db = mysql.connector.connect(host='	127.0.0.1', database='world', user='root', password='')
    #if db.is_connected():
        #print("CONNECTED TO MYSQL DATABASE!")
        #cur = db.cursor()
    #q = "SELECT name, population FROM country WHERE population>20000000;"
    #cur.execute(q)
    #for (name, population) in cur:
        #print("{} {}".format(name, population))

#except Error as e:
    #print(e)
#finally:
    #db.close()
    #print("DATABASE CONNECTION CLOSED!")