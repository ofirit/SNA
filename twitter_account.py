import tweepy as tw
import re
import io
import csv
from tweepy import OAuthHandler
import Utils
import json
import elastic2

consumer_key = "oImbQSGr6eQmuVtJDfLxUf6AQ"
consumer_secret = "9GgY6XiLDyHItX0kY8ypJRGZDcBr1lK9rdXYj9UvP3CW7MVg2E"

access_token = "1204366824353226752-gHhuzRaQJPG8C6w4I98TLI5YSjWhWH"
access_token_secret = "FUCPjicyAzIKoXBhRzRUWI6gvEiatCRsaC9yVRUmVQLWW"


TEL_AVIV = {
    'lat': 32.085300,
    'long': 34.781769
}

class TwitterAccount:

    def __init__(self):
        # Authorize twitter, initialize tweepy
        auth = tw.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tw.API(auth, wait_on_rate_limit=True)

    def run(self):
        twitter_account = TwitterAccount()

        try:
            twitter_account.api.verify_credentials()
            print("Authentication OK")

        except:
            print("Error during authentication")

        api = twitter_account.api

        # res = Utils.get_tweet(api, words='Yoav')
        # res = Utils.get_tweet_by_word(api, '"bibi Netanyahu"',12)

        res = Utils.get_tweet(api, lat=TEL_AVIV['lat'], long=TEL_AVIV['long'], radios=200, words="")
        a = 0
        print(res)

        for r in res:
            a = a + 1
            #print(r, " ", a)
            # elastic2.send_data_to_es(r, a + 2000)
        # Utils.write_to_csv(res, 'Tweets')
        Utils.write_to_json("Tweets.json", res)


if __name__ == '__main__':
    b = TwitterAccount()
    b.run()