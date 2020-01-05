import tweepy
from General import *
from datetime import datetime
from data_handler import *

# Global variables

# Twitter API credentials
consumer_key = "oImbQSGr6eQmuVtJDfLxUf6AQ"
consumer_secret = "9GgY6XiLDyHItX0kY8ypJRGZDcBr1lK9rdXYj9UvP3CW7MVg2E"

access_key = "1204366824353226752-gHhuzRaQJPG8C6w4I98TLI5YSjWhWH"
access_secret = "FUCPjicyAzIKoXBhRzRUWI6gvEiatCRsaC9yVRUmVQLWW"


class TwitterDeveloperAccount(object):

    def __init__(self):
        # Authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)

        # Data
        self.tweets_list = []
        self.publishers_list = []
        self.tweets_for_train_list = []
        self.publishers_for_train = []

        self.tables = ["publishers", "tweets", "tweets_for_train", "publishers_for_train"]

def get_friends_by_id(self, screen_name):
    ids = []
    for page in tweepy.Cursor(self.api.followers_ids, screen_names=[screen_name]).pages():
        ids.extend(page)
    return ids
    # screen_names = [user.screen_name for user in self.api.lookup_users(user_ids=ids)]


def get_tweet_by_id(self, wanted_tweets_id):
    tweets_itr = self.api.statuses_lookup(wanted_tweets_id)
    tweets_for_train_list = []
    publishers_for_train = []

    for tweet_i in tweets_itr:
        mention_tweet = tweet_i._json
        # mention_tweet.pop("user", None)
        mention_tweet.pop("id", None)
        tweet_id = mention_tweet.pop("id_str", None)
        mention_tweet["tweet_id"] = tweet_id
        tweets_for_train_list.append(mention_tweet)

        publisher = tweet_i.author._json
        publisher_id = publisher["id"]
        publisher.pop("id", None)
        publisher.pop("id_str", None)
        publisher["publisher_id"] = publisher_id
        publishers_for_train.append(publisher)

    # TODO: write
    write_to_csv(tweets_for_train_list, "tweets_for_train_list")
    write_to_csv(publishers_for_train, "publishers_for_train")
    return tweets_for_train_list, publishers_for_train, True


# def send_data(self, table_name):
#     # insert_tweets(self.tweets_list)
#     if table_name not in self.tweets_list:
#         print("Table name does not exist please use send_new_data()")
#         raise Exception
#         return
#
#     if table_name == "publishers" and len(self.publishers_list) != 0:
#         insert(table_name, self.publishers_list)
#     elif table_name == "tweets" and len(self.tweets_list) != 0:
#         insert(table_name, self.tweets_list)
#     elif table_name == "tweets_for_train" and len(self.tweets_for_train_list) != 0:
#         insert(table_name, self.tweets_for_train_list)
#     elif table_name == "publishers_for_train" and len(self.publishers_for_train) != 0:
#         insert(table_name, self.publishers_for_train)
#     else:
#         print(f"{table_name} list is empty!")
#
#     return


def get_mentions(self, max_time_in_seconds=3600 * 24):
    """

    :param max_time_in_seconds: Default = 3600
    :return:
    """
    current_timestamp = datetime.now()

    def mention_not_relevant(mention_timestamp):
        time_delta = current_timestamp - mention_timestamp
        return time_delta.total_seconds() > max_time_in_seconds

    def fill_tweets_dict(mention_tweet_, publisher_id):
        mention_tweet = mention_tweet_._json
        mention_tweet.pop("user", None)
        mention_tweet.pop("id", None)
        tweet_id = mention_tweet.pop("id_str", None)

        mention_tweet["tweet_id"] = tweet_id
        mention_tweet["publisher_id"] = publisher_id
        self.tweets_list.append(mention_tweet)

    def fill_publisher_dict(mention_user_, publisher_id):
        mention_publisher = mention_user_.user._json
        mention_publisher.pop("id", None)
        mention_publisher.pop("id_str", None)

        mention_publisher["publisher_id"] = publisher_id
        self.publishers_list.append(mention_publisher)

    for mentions in tweepy.Cursor(self.api.mentions_timeline).items():
        # If more then needed time
        mention_timestamp = mentions.created_at
        hour = mention_timestamp.hour + 3
        mention_timestamp = mention_timestamp.replace(tzinfo=None)
        mention_timestamp = mention_timestamp.replace(hour=hour)
        if mention_not_relevant(mention_timestamp):
            break

        # Publisher id as primary key
        publisher_id = mentions.user._json["id"]

        fill_publisher_dict(mentions, publisher_id)
        fill_tweets_dict(mentions, publisher_id)

    write_to_csv(self.tweets_list, "tweets")
    write_to_csv(self.publishers_list, "publishers")

    self.send_data("publishers")
    self.send_data("tweets")


def get_all_tweets(self, id="", user_id="", screen_name=""):
    if id == "" and user_id == "" and screen_name == "":
        print("Usage")
        return

    # Initialize a list to hold all the tweepy Tweets
    all_tweets = []

    # Make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = self.api.user_timeline(screen_name=screen_name, count=200)

    # Save most recent tweets
    all_tweets.extend(new_tweets)

    # Save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1

    # Keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # All subsiquent requests use the max_id param to prevent duplicates
        new_tweets = self.api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # Save most recent tweets
        all_tweets.extend(new_tweets)

        # Update the id of the oldest tweet less one
        oldest = all_tweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(all_tweets)))

    print("Writing all tweets to csv")
    # Transform the tweepy tweets into a 2D array that will populate the csv
    out_tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in all_tweets]
    write_to_csv(out_tweets, screen_name=screen_name)