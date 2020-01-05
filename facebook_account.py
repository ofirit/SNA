# token: EAAGVfCGky9sBAIxq9PgIi5hgudGRLa1emgzZAggrlpWfXPXW5vm5bQmQ3W9e73mKF9mx6ZCFlbsDFkA0GmtqLENdswEoOzWFDgLg2mSOfRsvD7wjNjPUVnn7t4JZAZCwN0CAfBmum5B5QK1U4CCpufyJbfauPyJqkse0vEUWWt4nGkPiG8SjDYMMh7TYjmlOR0gcgyruWgZDZD
import os
import json
import facebook
import twitter_account

if __name__ == '__main__':
    #token = os.environ.get('FACEBOOK_TEMP_TOKEN')
    token = 'EAAGVfCGky9sBAHELzdyOm5j6YOZBMRvl5F8gBaG14P3hwc1jD6Cuu5NZA99UClGQXHezZBqJRhK7O1HwKKJ9JgIsfX1ZBtTMowbgIVTnff0CZBhZCDbZBhcbemROHPMphN8ZBHFiM9jAUdcxCaYSyEMgu9DVxtBDPg0LUbjZACZCqwJgZDZD'
    graph = facebook.GraphAPI(token)
    print('OK')


    user = graph.get_object("me")

    # self profile
    profile = graph.get_object(user['id'], fields='name{},email')

    #places =  graph.search(type='place',
     #                 center='32.085300, 34.781769',
     #                 fields='name,location')

    #friends

    friends = graph.get_connections('me', "friends")

    #posts
    posts = graph.get_connections('me', "posts")

    print(json.dumps(profile, indent=4))
    #print(json.dumps(places, indent=4))
    print(json.dumps(friends, indent=4))
    print(json.dumps(posts, indent=4))
