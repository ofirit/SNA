import elastic2
import twitter_account

locations = [
    {'location_code': 'TA', 'lat': 32.085300, 'long': 34.811409, 'radios': 5.5},
    {'location_code': 'HOLON', 'lat': 32.002849, 'long': 34.778214, 'radios': 5.0},
    {'location_code': 'HERZELIYA', 'lat': 32.169051, 'long': 34.862736, 'radios': 6.0},
    {'location_code': 'REHOVOT', 'lat': 31.912339, 'long': 34.802501, 'radios': 6.0},
    {'location_code': 'BEITSHEMESH', 'lat': 31.752787, 'long': 34.979741, 'radios': 20.0},
    {'location_code': 'LACHISH', 'lat': 31.515607, 'long': 34.780647, 'radios': 15.0},
    {'location_code': 'RAMATNEGEV', 'lat': 30.583785, 'long': 34.898294, 'radios': 35.0},
    {'location_code': 'HEVELEILOT', 'lat': 30.195234, 'long': 34.903787, 'radios': 35.0},
    {'location_code': 'HEVELEILOT-S', 'lat': 29.835260, 'long': 34.995885, 'radios': 35.0}
]

ta = twitter_account.TwitterAccount()
ta.run()

es = elastic2.ElasticSearchClass()


for location in locations:
    tweets = ta.get_filtered_tweets(lat=location['lat'], long=location['long'], location_code=location['location_code'], radios=location['radios'], query="likod OR ליכוד OR נתניהו OR ביבי OR bibi OR netanyahu OR نتانياهو", num_of_results=1500)
    print(tweets)
    for status in tweets:
        es.send_data_to_es(data=status, index_name='tweets_areas2')
