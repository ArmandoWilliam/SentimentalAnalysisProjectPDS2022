import time
import tweepy
from mysql.connector import Error
from textblob import TextBlob
import re
import mysql.connector

# Authentication
consumerKey = 'QRqfS9CB0HVIRc4quS87IZHNG'
consumerSecret = 'LmVxOncvxtYHk9oodKhC1DXiLnfiGj5DynsUhRpwHQ0mxPltDS'
accessToken = '774595740-zPtsJk7CacapPzigJlNY5ogSXlPkGMR9BGjVCnQi'
accessTokenSecret = 'P6oKNReEFXx0dx0rCNj4s4y2MjUfvRLkJ9YpMRw69Xwre'
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


def clean_tweet(tweet):
    return ''.join(
        re.sub(r"(@[A-Za-z0-9_]+)|(#[A-Za-z0-9_]+)|(http\S+)|(www.\S+)|([^0-9A-Za-z\t])|(\w+:\/\/\S+)", " ", tweet))


def get_tweet_sentiment(tweet):
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    time.sleep(10)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def join_hstg(hstg):
    return ' '.join(hstg)


fetch_tweets = []
players = ['Djokovic', 'Tsitsipas', 'Nadal']
limit = 1000

try:
    db = mysql.connector.connect(host='	127.0.0.1', database='twitterdb', user='root', password='f18_kd0=?')
    if db.is_connected():
        print("connected to mysql database!")
        cur = db.cursor()
    q = """INSERT INTO
           tweet_sentiment (searchParam, user_name, text, hashtags, date, location, number_of_followers, number_of_tweets, number_of_account_retweets, sentiment)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    for player in players:
        counter = limit
        tweets = tweepy.Cursor(api.search_tweets, q=player + '-filter:retweets', count=100, tweet_mode='extended',
                               lang="en").items(limit)
        for tweet in tweets:
            # find the hashtags in the tweet
            hstgs = []
            for hstg in tweet.entities['hashtags']:
                hstgs.append(hstg['text'])

            # ------------------------------------ WITH THE DATAFRAME ----------------------------------------------#

            #                tweet_dict = {'searchParam': player,
            #                              'user_name': tweet.user.screen_name,
            #                              'text': clean_tweet(tweet.full_text),
            #                              'hashtags': join_hstg(hstgs),
            #                              'date': tweet.created_at,
            #                              'location': tweet.user.location,
            #                              'number_of_followers': tweet.user.followers_count,
            #                              'number_of_tweets': tweet.user.statuses_count,
            #                              'number_of_account_retweets': tweet.retweet_count,
            #                              'sentiment': get_tweet_sentiment(tweet.full_text)
            #                              }

            #                fetch_tweets.append(tweet_dict)
            #                df_tweets = pd.DataFrame(fetch_tweets)
            # print(df_tweets)

            # ------------------------------------ WITH THE DATAFRAME ----------------------------------------------#

            user_name = tweet.user.screen_name
            text = clean_tweet(tweet.full_text)
            hashtags = join_hstg(hstgs)
            date = tweet.created_at
            location = tweet.user.location
            number_of_followers = tweet.user.followers_count
            number_of_tweets = tweet.user.statuses_count
            number_of_account_retweets = tweet.retweet_count
            sentiment = get_tweet_sentiment(tweet.full_text)

            insert_tuple = (player, user_name, text, hashtags, date, location, number_of_followers, number_of_tweets,
                            number_of_account_retweets, sentiment)
            result = cur.execute(q, insert_tuple)
            db.commit()
            print(f'Record inserted successfully into tweets_table table still {counter} record to insert')
            counter -= 1

except Error as error:
    db.rollback()
    print('Failed to insert into MySQL table {db}'.format(error))

finally:
    # closing database connection.
    if db.is_connected():
        cur.close()
        db.close()
        print("MySQL connection is closed")

# ------------------------------------ WITH THE DATAFRAME ----------------------------------------------#

# create sqlalchemy engine
# engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
#                       .format(user="root",
#                               pw="f18_kd0=?",
#                               db="twitterdb"))

# Insert whole DataFrame into MySQL
# df_tweets.to_sql('tweet_sentiment', con = engine, index = False if_exists = 'append', chunksize = 1000)

# ------------------------------------ WITH THE DATAFRAME ----------------------------------------------#