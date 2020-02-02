from typing import Dict

import elastic2
import twitter_account
import Utils

locations = [
    {'location_code': 'Eliat', 'lat': 29.875702, 'long': 34.958404, 'radios': 43.530},
    {'location_code': 'Negev', 'lat': 30.878236, 'long': 34.867489, 'radios': 65.140},
    {'location_code': 'Ashdod-Ashkelon', 'lat': 31.684079, 'long': 34.728033, 'radios': 22.280},
    {'location_code': 'DeadSea', 'lat': 31.498442, 'long': 35.343956, 'radios': 17.644},
    {'location_code': 'Jerusalem', 'lat': 31.740343, 'long': 35.127538, 'radios': 15.389},
    {'location_code': 'WestBank', 'lat': 31.922449, 'long': 35.372519, 'radios': 15.148},
    {'location_code': 'Lod-Modiin', 'lat': 31.934996, 'long': 35.009428, 'radios': 9.030},
    {'location_code': 'Rishon', 'lat': 31.951905, 'long': 34.795682, 'radios': 9.021},
    {'location_code': 'TelAviv', 'lat': 32.084554, 'long': 34.770754, 'radios': 5.647},
    {'location_code': 'PetahTikve', 'lat': 32.065936, 'long': 34.913747, 'radios': 8.242},
    {'location_code': 'Hasharon-Caesarea', 'lat': 32.407973, 'long': 34.802259, 'radios': 31.069},
    {'location_code': 'Haifa-Naharia', 'lat': 32.835003, 'long': 35.021563, 'radios': 22.810},
    {'location_code': 'Tibirias-Nazarath', 'lat': 32.725694, 'long': 35.500, 'radios': 25.238},
    {'location_code': 'Qiryat Shemona', 'lat': 32.725694, 'long': 35.500484, 'radios': 25.238}
]

ta = twitter_account.TwitterAccount()
ta.run()

es = elastic2.ElasticSearchClass()

# words="likud OR likod OR ליכוד OR נתניהו OR ביבי OR bibi OR netanyahu OR نتانياهو", num_of_results=1500)
# words=['Bibi', 'Netanyahu', 'نتانياهو', 'بنيامين', 'ביבי' ,'נתניהו'], num_of_res=100)

index_name = 'israel_locations5'
#es.send_data_to_es(data=None, index_name=index_name)

for location in locations:
    tweets = Utils.get_tweet(ta.api, lat=location['lat'], long=location['long'],
                             location_code=location['location_code'], radios=location['radios'],
                             words="Bibi OR ביבי",
                             num_of_res=1000, es=es, index_name=index_name)
    for tweet in tweets:
        es.send_data_to_es(data=tweet, index_name=index_name)
