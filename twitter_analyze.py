# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:41:26 2017

A scripts to analyze tweets data.

@author: 5004756
"""

import json
import pandas as pd
import matplotlib.pyplot as plt

# Read the data into an array called tweets_data
#tweets_data_path = './data/stream_data.txt'
tweets_data_path = './data/search_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")


for line in tweets_file:
    
    if len(line) > 10:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except ValueError as err:
            print(err)
            #continue
            break

print(len(tweets_data))

tweetDF = pd.DataFrame()

tweetDF['id'] = map(lambda t : t['id'], tweets_data)
tweetDF['created_at'] = map(lambda t : t['created_at'], tweets_data)
tweetDF['text'] = map(lambda t : t['text'], tweets_data)
tweetDF['country'] = map(lambda t : t['place']['country'] if t['place'] != None else None, tweets_data)
tweetDF['retweet_count'] = map(lambda t : t['retweet_count'], tweets_data)
tweetDF['favorite_count'] = map(lambda t : t['favorite_count'], tweets_data)
tweetDF['userId'] = map(lambda t : t['user']['id'], tweets_data)
tweetDF['userName'] = map(lambda t : t['user']['screen_name'], tweets_data)

tweets_by_country = tweetDF['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')