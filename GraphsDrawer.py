import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
# from TwitterFetcher import players
from datetime import datetime

players = ['Djokovic', 'Tsitsipas', 'Nadal']


# method to draw a timeline with sentiment associated to the relative dates, for a single player
def draw_datetime_sentiment(list_of_date_sentiment, tennis_playre_name, sentiment):
    figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Percentage of " + sentiment + " tweets for " + tennis_playre_name)
    axes.bar(
        range(len(list_of_date_sentiment)),
        [sentiment[1] for sentiment in list_of_date_sentiment],
        tick_label=[date[0] for date in list_of_date_sentiment]
    )
    return figure

def draw_datetime_sentiment_influencer(list_of_date_sentiment, tennis_playre_name, sentiment):
    figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.set_title("Retweets of influencer tweets for " + tennis_playre_name + " with a " + sentiment + " sentiment")
    axes.bar(
        range(len(list_of_date_sentiment)),
        [sentiment[1] for sentiment in list_of_date_sentiment],
        tick_label=[date[0] for date in list_of_date_sentiment]
    )
    return figure


def sentiment_counter_by_date_dic_modifier(date, dict_of_dates):
    if date in dict_of_dates:
        dict_of_dates[date] += 1
    else:
        dict_of_dates[date] = 0


def sentiment_percentage_dic_modifier(dict_of_dates, total_sentiment_counter):
    for date_key in dict_of_dates:
        date_total = dict_of_dates.get(date_key)
        try:
            dict_of_dates[date_key] = 100 * (date_total / total_sentiment_counter)
        except ZeroDivisionError as e:
            print(e)



try:
    db = mysql.connector.connect(host='	127.0.0.1', database='twitterdb', user='root', password='f18_kd0=?')
    if db.is_connected():
        print("CONNECTED TO MYSQL DATABASE!")
        cur = db.cursor()

        #Get the toal of neutral, positive and negative tweets
        q = "SELECT searchParam, sentiment FROM tweet_sentiment;"
        cur.execute(q)
        total_neutral_counter = 0
        total_positive_counter = 0
        total_negative_counter = 0
        for (searchParam, sentiment) in cur:
            if sentiment == "neutral":
                total_neutral_counter += 1
            elif sentiment == "positive":
                total_positive_counter += 1
            elif sentiment == "negative":
                total_negative_counter += 1

        # Djokovic counter of tweets sentiments
        q = "SELECT searchParam, sentiment FROM tweet_sentiment WHERE searchParam = 'Djokovic';"
        cur.execute(q)
        neutral_counter = 0
        positive_counter = 0
        negative_counter = 0
        for (searchParam, sentiment) in cur:
            if sentiment == "neutral":
                neutral_counter += 1
            elif sentiment == "positive":
                positive_counter += 1
            elif sentiment == "negative":
                negative_counter += 1
        figure = plt.figure()
        axes = figure.add_subplot(1, 1, 1)
        axes.set_title('Djokovic tweets counter')
        axes.bar([1, 2, 3], [neutral_counter, positive_counter, negative_counter],
                 tick_label=["Neutral", "Positive", "Negative"])
        plt.show()

        # Tsitsipas counter of tweets sentiments
        q = "SELECT searchParam, sentiment FROM tweet_sentiment WHERE searchParam = 'Tsitsipas';"
        cur.execute(q)
        neutral_counter = 0
        positive_counter = 0
        negative_counter = 0
        for (searchParam, sentiment) in cur:
            if sentiment == "neutral":
                neutral_counter += 1
            elif sentiment == "positive":
                positive_counter += 1
            elif sentiment == "negative":
                negative_counter += 1
        figure = plt.figure()
        axes = figure.add_subplot(1, 1, 1)
        axes.set_title('Tsitsipas tweets counter')
        axes.bar([1, 2, 3], [neutral_counter, positive_counter, negative_counter],
                 tick_label=["Neutral", "Positive", "Negative"])
        plt.show()

        # Nadal counter of tweets sentiments
        q = "SELECT searchParam, sentiment FROM tweet_sentiment WHERE searchParam = 'Nadal';"
        cur.execute(q)
        neutral_counter = 0
        positive_counter = 0
        negative_counter = 0
        for (searchParam, sentiment) in cur:
            if sentiment == "neutral":
                neutral_counter += 1
            elif sentiment == "positive":
                positive_counter += 1
            elif sentiment == "negative":
                negative_counter += 1
        figure = plt.figure()
        axes = figure.add_subplot(1, 1, 1)
        axes.set_title('Nadal tweets counter')
        axes.bar([1, 2, 3], [neutral_counter, positive_counter, negative_counter],
                 tick_label=["Neutral", "Positive", "Negative"])
        plt.show()

        # Plot a timeline tweets sentiment for Nadal
        q = "SELECT searchParam, tweet_sentiment.date, sentiment FROM tweet_sentiment WHERE searchParam = 'Nadal';"
        cur.execute(q)
        dates_dic_Nadal_neutral = {}
        dates_dic_Nadal_positive = {}
        dates_dic_Nadal_negative = {}

        for (searchParam, date, sentiment) in cur:
            date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if sentiment == "neutral":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Nadal_neutral)
            elif sentiment == "positive":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Nadal_positive)
            elif sentiment == "negative":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Nadal_negative)

        sentiment_percentage_dic_modifier(dates_dic_Nadal_neutral, total_neutral_counter)
        sentiment_percentage_dic_modifier(dates_dic_Nadal_positive, total_positive_counter)
        sentiment_percentage_dic_modifier(dates_dic_Nadal_negative, total_negative_counter)

        draw_datetime_sentiment(dates_dic_Nadal_neutral.items(), 'Nadal', 'Neutral')
        draw_datetime_sentiment(dates_dic_Nadal_positive.items(), 'Nadal', 'Positive')
        draw_datetime_sentiment(dates_dic_Nadal_negative.items(), 'Nadal', 'Negative')
        plt.show()

        # Plot a timeline tweets sentiment for Tsitsipas
        q = "SELECT searchParam, tweet_sentiment.date, sentiment FROM tweet_sentiment WHERE searchParam = 'Tsitsipas';"
        cur.execute(q)
        dates_dic_Tsitsipas_neutral = {}
        dates_dic_Tsitsipas_positive = {}
        dates_dic_Tsitsipas_negative = {}

        for (searchParam, date, sentiment) in cur:
            date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if sentiment == "neutral":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Tsitsipas_neutral)
            elif sentiment == "positive":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Tsitsipas_positive)
            elif sentiment == "negative":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Tsitsipas_negative)

        sentiment_percentage_dic_modifier(dates_dic_Tsitsipas_neutral, total_neutral_counter)
        sentiment_percentage_dic_modifier(dates_dic_Tsitsipas_positive, total_positive_counter)
        sentiment_percentage_dic_modifier(dates_dic_Tsitsipas_negative, total_negative_counter)

        draw_datetime_sentiment(dates_dic_Tsitsipas_neutral.items(), 'Tsitsipas', 'Neutral')
        draw_datetime_sentiment(dates_dic_Tsitsipas_positive.items(), 'Tsitsipas', 'Positive')
        draw_datetime_sentiment(dates_dic_Tsitsipas_negative.items(), 'Tsitsipas', 'Negative')
        plt.show()

        # Plot a timeline tweets sentiment for Djokovic
        q = "SELECT searchParam, tweet_sentiment.date, sentiment FROM tweet_sentiment WHERE searchParam = 'Djokovic';"
        cur.execute(q)
        dates_dic_Djokovic_neutral = {}
        dates_dic_Djokovic_positive = {}
        dates_dic_Djokovic_negative = {}

        for (searchParam, date, sentiment) in cur:
            date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if sentiment == "neutral":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Djokovic_neutral)
            elif sentiment == "positive":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Djokovic_positive)
            elif sentiment == "negative":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Djokovic_negative)

        sentiment_percentage_dic_modifier(dates_dic_Djokovic_neutral, total_neutral_counter)
        sentiment_percentage_dic_modifier(dates_dic_Djokovic_positive, total_positive_counter)
        sentiment_percentage_dic_modifier(dates_dic_Djokovic_negative, total_negative_counter)

        print(f"The neutral tweets are in total: {total_neutral_counter}")
        for date_key in dates_dic_Djokovic_neutral.keys():
            print(f"The percentage of neutral tweets for the date {date_key} Djokovic is {dates_dic_Djokovic_neutral.get(date_key)}")

        draw_datetime_sentiment(dates_dic_Djokovic_neutral.items(), 'Djokovic', 'Neutral')
        draw_datetime_sentiment(dates_dic_Djokovic_positive.items(), 'Djokovic', 'Positive')
        draw_datetime_sentiment(dates_dic_Djokovic_negative.items(), 'Djokovic', 'Negative')
        plt.show()

        #timeline with number of retweets about Nadal, made from the hight impact accounts (more than 10000 folloers) related to the sentiment of the tweet
        q = "SELECT searchParam, tweet_sentiment.date, sentiment FROM tweet_sentiment WHERE searchParam = 'Nadal' and number_of_followers > 10000;"
        cur.execute(q)
        dates_dic_Nadal_neutral = {}
        dates_dic_Nadal_positive = {}
        dates_dic_Nadal_negative = {}

        for (searchParam, date, sentiment) in cur:
            date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if sentiment == "neutral":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Nadal_neutral)
            elif sentiment == "positive":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Nadal_positive)
            elif sentiment == "negative":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Nadal_negative)

        draw_datetime_sentiment_influencer(dates_dic_Nadal_neutral.items(), 'Nadal', 'Neutral')
        draw_datetime_sentiment_influencer(dates_dic_Nadal_positive.items(), 'Nadal', 'Positive')
        draw_datetime_sentiment_influencer(dates_dic_Nadal_negative.items(), 'Nadal', 'Negative')
        plt.show()

        #timeline with number of retweets about Tsitsipas, made from the hight impact accounts (more than 10000 folloers) related to the sentiment of the tweet
        q = "SELECT searchParam, tweet_sentiment.date, sentiment FROM tweet_sentiment WHERE searchParam = 'Tsitsipas' and number_of_followers > 10000;"
        cur.execute(q)
        dates_dic_Tsitsipas_neutral = {}
        dates_dic_Tsitsipas_positive = {}
        dates_dic_Tsitsipas_negative = {}

        for (searchParam, date, sentiment) in cur:
            date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if sentiment == "neutral":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Tsitsipas_neutral)
            elif sentiment == "positive":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Tsitsipas_positive)
            elif sentiment == "negative":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Tsitsipas_negative)

        draw_datetime_sentiment_influencer(dates_dic_Tsitsipas_neutral.items(), 'Tsitsipas', 'Neutral')
        draw_datetime_sentiment_influencer(dates_dic_Tsitsipas_positive.items(), 'Tsitsipas', 'Positive')
        draw_datetime_sentiment_influencer(dates_dic_Tsitsipas_negative.items(), 'Tsitsipas', 'Negative')
        plt.show()

        # timeline with number of retweets about Djokovic, made from the hight impact accounts (more than 10000 folloers) related to the sentiment of the tweet
        q = "SELECT searchParam, tweet_sentiment.date, sentiment FROM tweet_sentiment WHERE searchParam = 'Djokovic' and number_of_followers > 10000;"
        cur.execute(q)
        dates_dic_Djokovic_neutral = {}
        dates_dic_Djokovic_positive = {}
        dates_dic_Djokovic_negative = {}

        for (searchParam, date, sentiment) in cur:
            date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            if sentiment == "neutral":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Djokovic_neutral)
            elif sentiment == "positive":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Djokovic_positive)
            elif sentiment == "negative":
                sentiment_counter_by_date_dic_modifier(date_time_obj.date(), dates_dic_Djokovic_negative)

        draw_datetime_sentiment_influencer(dates_dic_Djokovic_neutral.items(), 'Djokovic', 'Neutral')
        draw_datetime_sentiment_influencer(dates_dic_Djokovic_positive.items(), 'Djokovic', 'Positive')
        draw_datetime_sentiment_influencer(dates_dic_Djokovic_negative.items(), 'Djokovic', 'Negative')
        plt.show()

except Error as error:
    db.rollback()
    print('Failed to insert into MySQL table {db}'.format(error))

finally:
    # closing database connection.
    if db.is_connected():
        cur.close()
        db.close()
        print("MySQL connection is closed")
