from textblob import TextBlob
import tweepy
from tweepy import OAuthHandler
import pandas as pd
from textblob import TextBlob
import re
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import pymysql

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
limit=100
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
            'number_of_tweets':tweet.user.statuses_count,
            'number_of_account_retweets':tweet.retweet_count,
            'sentiment':get_tweet_sentiment(tweet.full_text)
            }

        fetch_tweets.append(tweet_dict)


df_tweets = pd.DataFrame(fetch_tweets)

#print(df_tweets)

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="twitterdb"))

# Insert whole DataFrame into MySQL
df_tweets.to_sql('tweet_sentiment', con = engine, index=False,  if_exists = 'append', chunksize = 1000)

#try:
#    db = mysql.connector.connect(host='	127.0.0.1', database='twitterdb', user='root', password='f18_kd0=?')
#    if db.is_connected():
#        print("connected to mysql database!")
#        cur = db.cursor()
#    q = "insert into tweet_sentiment (user_name, text, hashtags, date, location, number_of_followers, number_of_tweets, number_of_account_retweets, sentiment) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#    cur.execute(q)

#except error as e:
#    print(e)
#finally:
#    db.close()
#    print("database connection closed!")