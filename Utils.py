import json
import csv

TWEET_KEYS = ['created_at', 'user', 'id', 'source', 'truncated', 'in_reply_to_status_id',
              'in_reply_to_user_id', 'lang', 'retweeted', 'is_quote_status', 'entities', 'retweet_count',
              'coordinates', 'place', 'text']


def get_tweet(api, lat=None, long=None, radios=1, words="", num_of_res=10000,
              until=None, include_replays=False, include_retweets=False, location_code=None):
    res_count = 0
    geo_code = "%f,%f,%dkm" % (lat, long, radios) if (lat and long) else None
    query = []
    tweets = []
    last_id = None
    query = ['1']
    while num_of_res > res_count and len(query) > 0:
        try:
            query = api.search(q=words, count=100, geocode=geo_code, until=until,
                               max_id=last_id)
            for status in query:
                # filter replays
                if (status.in_reply_to_status_id is None or include_replays) and \
                        ('RT @' not in status.text or include_retweets):
                    tweets.append(filter_status(status._json, location_code=location_code))
                    res_count += 1
                    if res_count == num_of_res:
                        break
                last_id = status.id - 1
        except Exception as e:
            print('error')
    return tweets


def filter_status(status, location_code=None):
    """
    this function gets status and filter it
    by the relevant keys that we want to save.
    :param location_code:
    :param status: status in json format
    :return: dict: filtered status in dict format
    """
    dict = {}
    for att in TWEET_KEYS:
        if att == 'user':
            dict['user_id'] = status[att]['id']
            continue
        if att == 'entities':
            dict['hashtags'] = status[att]['hashtags']
            continue
        if att == 'place':
            dict['place_id'] = status[att]['id'] if status[att] else None
            continue
        dict['location_code'] = location_code

        dict[att] = status[att]
    return dict


def write_to_json(file_name, res):
    with open(file_name, "w") as write_file:
        json.dump(res, write_file, indent=4)


def write_to_csv(list_to_write, file_name):
    with open('%s_tweets.csv' % file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'text'])
        writer.writerows(list_to_write)
