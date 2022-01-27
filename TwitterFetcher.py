from textblob import TextBlob
import tweepy
from tweepy import OAuthHandler
import pandas as pd

# Authentication
consumerKey = 'flKUc2Kf4UCMgWwSY59tjQxxp'
consumerSecret = 'Fkkd7jA612jNOf6nva0qealFZsYfP06GR8LoeratMEDPZHWxra'
accessToken = '1482383090274254864-O1c4tZmJrEzquTb8tcivg64c1MjUjy'
accessTokenSecret = '1axxDUDeLegFFep1077MH4nGTPfhHqIBz6sPD3gG6ajCr'
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
