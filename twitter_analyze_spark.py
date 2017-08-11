# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:41:26 2017

A scripts to analyze tweets data.

@author: 5004756
"""

import json

#==============================================================================
# # Step 1: Read the tweets data from files into a list called tweets_data
#==============================================================================

file_paths = ['./data/search_data_04.txt', './data/search_data_03.txt',
                     './data/search_data_02.txt', './data/search_data_01.txt']

tweets_data = []

for filepath in file_paths:
    tweets_file = open(filepath, "r")
    #note in the file each line is one tweet
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

# save the tweet_data to a file
with open('./data/combined_data.txt', 'w') as outfile:
    for tw in tweets_data:
        line = json.dumps(tw) + '\n'
        outfile.write(line)
outfile.close
    
    
#==============================================================================
# # Step 2: after load tweets, print out one example using pprint
#==============================================================================
import pprint
pprint.pprint(tweets_data[0],depth=5, indent=2)
# we can also print out the text field of this tweet
print("================")
print(tweets_data[0]['text'])


#==============================================================================
# # Step 3: start a spark session and load tweets into spark dataset
#==============================================================================
from pyspark.sql import SparkSession
from pyspark.sql import Row

# Create a SparkSession (the config bit is only for Windows!), remember to stop it by the end
spark = SparkSession.builder.config("spark.sql.warehouse.dir", "file:///C:/temp").appName("TweetAnalysis").getOrCreate()
sc = spark.sparkContext

# function that extact major informaiton of the tweet and the user who posted the tweets:
#==============================================================================
# id - unique identification of tweet
# created_at - time the tweet was posted
# text - content of the tweet
# country - place of the world where the tweet posted
# retweet_count - number of times the tweets was retweeted
# favorite_count - number of time the tweets was favored
# userId - id of the user who posted this tweet
# userName - screen name of the user who posted this tweet
#==============================================================================
def fieldsMapper(tweet_json):
    created_at_timestr = tweet_json['created_at']
    created_date = created_at_timestr[4:10] + "," + created_at_timestr[-4:] # post date
    country = tweet_json['place']['country'] if tweet_json['place']!= None else None
    return Row(ID=str(tweet_json['id']), 
               created_at=created_date,
               text=str(tweet_json['text']),
               country=str(country),
               retweet_count=int(tweet_json['retweet_count']),
               favorite_count=int(tweet_json['favorite_count']),
               userId=str(tweet_json['user']['id']),
               userName=str(tweet_json['user']['screen_name'])
               )

# read combined file into string a rdd
RDD_strings = sc.textFile('./data/combined_data.txt')

# load each line of string back to json and extract selected fields
tweets = RDD_strings.map(json.loads).map(fieldsMapper)

# Convert it to a DataFrame
tweetsDF = spark.createDataFrame(tweets).cache()
tweetsDF.show()
#tweetsDataset.printSchema()

## Infer the schema, and register the DataFrame as a table.
#schemaPeople = spark.createDataFrame(people).cache()
#
## Load up our movie ID -> name dictionary
#nameDict = loadMovieNames()
#
## Get the raw data
#lines = spark.sparkContext.textFile("./ml-100k/u.data")
## Convert it to a RDD of Row objects
#movies = lines.map(lambda x: Row(movieID =int(x.split()[1])))
## Convert that to a DataFrame
#movieDataset = spark.createDataFrame(movies)
#
## Some SQL-style magic to sort all movies by popularity in one line!
#topMovieIDs = movieDataset.groupBy("movieID").count().orderBy("count", ascending=False).cache()
#
## Show the results at this point:
#
##|movieID|count|
##+-------+-----+
##|     50|  584|
##|    258|  509|
##|    100|  508|
#
#topMovieIDs.show()
#
## Grab the top 10
#top10 = topMovieIDs.take(10)
#
## Print the results
#print("\n")
#for result in top10:
#    # Each row has movieID, count as above.
#    print("%s: %d" % (nameDict[result[0]], result[1]))

# Stop the session
spark.stop()




#tweetDF = pd.DataFrame()
#
#tweetDF['id'] = map(lambda t : t['id'], tweets_data)
#tweetDF['created_at'] = map(lambda t : t['created_at'], tweets_data)
#tweetDF['text'] = map(lambda t : t['text'], tweets_data)
#tweetDF['country'] = map(lambda t : t['place']['country'] if t['place'] != None else None, tweets_data)
#tweetDF['retweet_count'] = map(lambda t : t['retweet_count'], tweets_data)
#tweetDF['favorite_count'] = map(lambda t : t['favorite_count'], tweets_data)
#tweetDF['userId'] = map(lambda t : t['user']['id'], tweets_data)
#tweetDF['userName'] = map(lambda t : t['user']['screen_name'], tweets_data)
#
#tweets_by_country = tweetDF['country'].value_counts()
#
#fig, ax = plt.subplots()
#ax.tick_params(axis='x', labelsize=15)
#ax.tick_params(axis='y', labelsize=10)
#ax.set_xlabel('Countries', fontsize=15)
#ax.set_ylabel('Number of tweets' , fontsize=15)
#ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
#tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')