import json
import csv

TWEET_KEYS = ['entities', 'created_at', 'user', 'id', 'source', 'truncated', 'in_reply_to_status_id',
              'in_reply_to_user_id', 'lang', 'retweeted', 'is_quote_status', 'retweet_count',
              'coordinates', 'place', 'text']

USER_KEYS = ["id", "name", "screen_name", "location", "followers_count", "friends_count", "listed_count",
             "statuses_count", "created_at", "time_zone", "lang", "following"]

ENTITIES_KEYS = ["hashtags", "media"]

PLACE_KEYS = ["place_type", "name", "id", "full_name", "country_code", "country", "bounding_box"]


def get_tweet(api, lat=None, long=None, radios=1, words="", num_of_res=10000,
              until=None, include_replays=False, include_retweets=False, location_code=None, es=None, index_name=None):

    res_count = 0
    geo_code = "%f,%f,%dkm" % (lat, long, radios) if (lat and long and radios) else None
    tweets = []
    last_id = None
    query = ['1']
    while num_of_res > res_count and len(query) > 0:
        try:
            query = api.search(q=words, count=100, geocode=geo_code, until=until,
                               max_id=last_id)
            for status in query:
                # filter replays and retweets
                if 'RT @' not in status.text or include_retweets:
                    if status.in_reply_to_status_id is None or include_replays:
                        if es.check_if_tweet_exists(data=status, index_name=index_name):
                            print('exists')
                            last_id = status.id - 1
                            continue
                        # adding the filtered status fields and the computed field location_code
                        tweets.append(filter_status(status._json, location_code=location_code, lat=lat, long=long))
                        res_count += 1
                        if res_count >= num_of_res:
                            break
                last_id = status.id - 1


        except Exception as e:
            print(e)
            print('Error getting tweets')
    return tweets


def get_hastages_list(status_hashtags):
    """this function gets only hashtag names
    from a status hashtag entry
    :param status_hashtags:
    :return: list of hashtags
    """
    hashtags = []
    for hashtag in status_hashtags:
        if 'text' in hashtag.keys():
            hashtags.append(hashtag['text'])
    return hashtags


def get_media_att(status_media):
    status_media = status_media[0]  # media field in status entities is a list

    media_type, media_url = status_media['type'], status_media['media_url']

    return media_type, media_url


def get_cordinents(status_bounding_box):
    coordinates = status_bounding_box['coordinates']
    type_ = status_bounding_box['type']
    return coordinates, type_


def filter_status(status, location_code=None, lat=None, long=None):
    """
    this function gets status and filter it
    by the relevant keys that we want to save.
    :param location_code:
    :param status: status in json format
    :return: dict: filtered status in dict format
    """
    tweets_dict = {}

    for att in TWEET_KEYS:
        if att == 'user':
            for key in USER_KEYS:
                tweets_dict[att + '_' + key] = status[att][key] if status[att] else None
            continue
        if att == 'entities':
            for key in ENTITIES_KEYS:
                if key == 'hashtags' and key in status[att].keys():
                    # tweets_dict[key] = get_hastages_list(status[att][key])
                    tweets_dict[key] = None
                    
                if key == 'media' and key in status[att].keys():
                    media_type, media_url = get_media_att(status[att][key])
                    tweets_dict['media_type'] = media_type
                    tweets_dict['media_url'] = media_url
                else:
                    tweets_dict['media_type'] = None
                    tweets_dict['media_url'] = None
            continue
        if att == 'place' and status[att]:
            for key in PLACE_KEYS:

                if key == "bounding_box" and key in status[att].keys():
                    coord, type_ = get_cordinents(status[att][key])
                    tweets_dict['coordinates'] = coord
                    tweets_dict['coordinates_type'] = type_
                else:
                    tweets_dict[att + '_' + key] = status[att][key] if (status[att] and key in status[att].keys()) else None
                continue

        tweets_dict[att] = status[att]
    tweets_dict['location_coordinates'] = [long, lat]
    tweets_dict['location_code'] = location_code
    return tweets_dict


def write_to_json(file_name, res):
    with open(file_name, "w") as write_file:
        json.dump(res, write_file, indent=4)


def write_to_csv(list_to_write, file_name):
    with open('%s_tweets.csv' % file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'text'])
        writer.writerows(list_to_write)
