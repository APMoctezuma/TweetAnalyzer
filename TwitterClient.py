import re
import tweepy
import pandas as pd
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    def __init__(self):
        consumer_key = 'uz4wSx2vt2PlKbWCOllpKbBZo'
        consumer_secret = 'lq61FxYRvJPwLjjRlUf0rSTsdX86iijHYeGfrUdi7EhZzWsWv'
        access_token = '1038510225786122247-zLnTCjChQ0rLUHevueL0CN4ygdY1Me'
        access_token_secret = 'W7lqUevzXRpzl4zQA6niMDR85r9SCo3sCQGaPA4wg6DS6'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive' + " " + analysis.sentiment.polarity
        elif analysis.sentiment.polarity == 0:
            return 'neutral' + " " + analysis.sentiment.polarity
        else:
            return 'negative' + " " + analysis.sentiment.polarity

    def get_tweets(self, query, count):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.txt
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.txt)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                return tweets
        except tweepy.TweepError as e:
            print("Error: " + str(e))


def main():
    api = TwitterClient()
    tweets = api.get_tweets(query='Rick Scott', count=15)
    df = pd.DataFrame(data=tweets)
    print(df.to_string())
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    for tweet in ptweets:
        print("Positive: " + tweet + "\n")
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    for tweet in ntweets:
        print("Negative: " + tweet + "\n")


if __name__ == "main":
    main()