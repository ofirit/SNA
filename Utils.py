import tweepy as tw
import csv
import Utils
import json
from elasticsearch import Elasticsearch

TWEET_KEYS = ['created_at','user', 'id', 'source', 'truncated', 'in_reply_to_status_id',
              'in_reply_to_user_id', 'lang', 'retweeted','is_quote_status',  'entities','retweet_count',
              'coordinates', 'place', 'text']



def get_tweet(api, lat=None, long=None, radios=1, words = "", num_of_res = 500,
              until=None, include_replays = False):
    res_count = 0
    geo_code = "%f,%f,%dkm" % (lat, long, radios) if lat and long else None
    query = []
    tweets = []
    last_id = None
    query = ['1']
    while (res_count < num_of_res and len(query) > 0):
        query = api.search(q=words, count=50, geocode=geo_code, until=until,
                                max_id=last_id)

        for staus in query:
            # filter replays
            if (staus.in_reply_to_status_id == None or include_replays):

                tweets.append(Utils.filter(staus._json))
            last_id = (staus.id) - 1

        res_count += len(query)

    return tweets


def get_hastages_list(status_hashtags):
    """this function gets only hastag names
    from a status hashtag entry
    :param status_hashtags:
    :return: list of hastags
    """
    hashtages = []
    for hastag in status_hashtags:
        hashtages.append(hastag['text'])
    return hashtages


def filter(status):
    """this function gets status and filter it
    by the relevant keys
    :param status: status in json format
    :return:
    """
    dict = {}
    for att in TWEET_KEYS:
        if att == 'user':
            dict['user_id'] = status[att]['id']
            continue
        if att == 'entities':
            dict['hashtags'] = get_hastages_list(status[att]['hashtags'])
            continue
        if att == 'place':
            dict['place_id'] = status[att]['id'] if status[att] else None
            continue

        dict[att] = status[att]
    return dict


def status_to_jason(status):
     j = json.dumps(status, indent=4)
     return j


def write_to(list_to_write, file_name):
    with open('%s_tweets.csv' % file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'text'])
        writer.writerows(list_to_write)






