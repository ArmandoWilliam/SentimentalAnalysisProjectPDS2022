import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

global get_tweet_sentiment
global TextBlob
global trim_tweet
global re

DEFAULT_ENCODING = 'utf-8'


def trim_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(trim_tweet(tweet).decode('ascii', 'ignore').encode("ascii"))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def get_tweets(api, query, count=10):
    # empty list to store parsed tweets
    tweets = []

    try:
        # call twitter api to fetch tweets
        fetched_tweets = api.search_tweets(q=query, count=count)

        # parsing tweets one by one
        for tweet in fetched_tweets:
            # empty dictionary to store required params of a tweet
            parsed_tweet = {}
            parsed_tweet['text'] = tweet.text.encode('utf-8')
            # saving sentiment of tweet
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text.encode('utf-8'))

            # appending parsed tweet to tweets list
            if tweet.retweet_count > 0:
                # if tweet has retweets, ensure that it is appended only once
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)

        # return parsed tweets
        return tweets

    except tweepy.errors.TweepError as e:
        # print error (if any)
        print("Error : " + str(e))


# keys and tokens from the Twitter Dev Console
consumer_key = 'dN0g9U8BVlURKs65o8rP5mnhE'
consumer_secret = 'pnsnUCnbDd1M1BIHg45IMi3IPbjaTkDXu6HLq9XNpiCB7fHiq6'
access_token = '1482383090274254864-8Hi0J2Bu4yBJcqUeJ2NjLSEd5ufAy1'
access_token_secret = 'aoUMItsal3nRxd2eDoI725SS7E4z1kOdMgK3XyQ1p24m8'

auth = OAuthHandler(consumer_key, consumer_secret)
# set access token and secret
auth.set_access_token(access_token, access_token_secret)
# create tweepy API object to fetch tweets
api = tweepy.API(auth)
tweets = get_tweets(api, query='Novak Djokovic', count=1000)
ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
# percentage of positive tweets
print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
# picking negative tweets from tweets
ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
# percentage of negative tweets
print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))

# printing first 5 positive tweets
print("\n\nPositive tweets:")
for tweet in ptweets[:5]:
    print(tweet['text'])

# printing first 5 negative tweets
print("\n\nNegative tweets:")
for tweet in ntweets[:5]:
    print(tweet['text'])
