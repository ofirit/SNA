import elastic2
import twitter_account

locations = [
    {'location_code': 'TA', 'lat': 32.085300, 'long': 34.781769}

            ]

ta = twitter_account.TwitterAccount()
ta.run()

es = elastic2.ElasticSearchClass()


for location in locations:
    tweets = ta.get_filtered_tweets(lat=location['lat'], long=location['long'], location_code=location['location_code'], radios=5, query="", num_of_results=10)
    print(tweets)
    for status in tweets:
        es.send_data_to_es(data=status, index_name='tweets')
