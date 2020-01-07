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

        self.api = twitter_account.api

    def get_filtered_tweets(self, lat, long, location_code, radios, query, num_of_results):
        res = Utils.get_tweet(self.api, lat=lat, long=long, radios=radios, words=query, num_of_res=num_of_results, location_code=location_code)
        a = 0
        return res

        # Utils.write_to_json("Tweets.json", res)


if __name__ == '__main__':
    b = TwitterAccount()
    b.run()
