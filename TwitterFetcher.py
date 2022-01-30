from textblob import TextBlob
import tweepy
from tweepy import OAuthHandler
import pandas as pd
from textblob import TextBlob
import re

# Authentication
consumerKey = ''
consumerSecret = ''
accessToken = ''
accessTokenSecret = ''
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


def clean_tweet(tweet):
    return ' '.join(re.sub(r"(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)|([^0-9A-Za-z \t])|(http\S+)|(www.\S+)", " ", tweet))

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

fetch_tweets = []
players = ['Nadal','Tsitsipas','Djokovic']
limit=1000
for player in players :
    tweets = tweepy.Cursor(api.search_tweets, q=player, count=100, tweet_mode='extended').items(limit)

    for tweet in tweets:
        # find the hashtags in the tweet
        hstgs = []
        for hstg in tweet.entities['hashtags']:
            hstgs.append(hstg['text'])

        tweet_dict = {'searchParam': player,
            'user_name': tweet.user.screen_name,
            'text': tweet.full_text,
            'hashtags': hstgs,
            'date': tweet.created_at,
            'location': tweet.user.location,
            'number_of_followers':tweet.user.followers_count,
            'number_of tweets':tweet.user.statuses_count,
            'sentiment':get_tweet_sentiment(tweet.full_text)
            }
        if tweet.retweet_count > 0:
            # if tweet has retweets, ensure that it is appended only once
            if tweet_dict not in tweets:
                fetch_tweets.append(tweet_dict)
        else:
            fetch_tweets.append(tweet_dict)


df_tweets = pd.DataFrame(fetch_tweets)
print(df_tweets)
