

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:47:29 2017

A scripts using Python library tweepy to connect to Twitter Search API 
and download data.

https://dev.twitter.com/rest/reference/get/search/tweets

@author: 5004756 Lei Feng
"""

# Import neccesary methods from tweepy library
import tweepy
import json
import argparse



# Global variables of user credentials to access Twitter API
# all information from "https://apps.twitter.com/app/13083667/keys" -LeiFengBlog
CONSUMER_KEY = "q1BbMVgJGpPZ3IVrCkmv1tcix"
CONSUMER_SECRET = "sfwpBjHPijxbjTBDyiOmFb5MxcGa3LaXUpim1NmbA1gWFfzVjK"
ACCESS_TOKEN = "770679954-vWDVGhFKOdwR1vzN56Cgcc2Rcf4QoGhCBPwOvcgd"
ACCESS_SECRET = "VKmuoM3wLDwT8QrOhyzE9ySIsZQnnEp4FSRGdXVLbTLSl"
SAVED_FILE_PATH = "./data/search_data_08.txt"


def get_args_parser():
    '''A function parse the arguments'''
    parser = argparse.ArgumentParser(add_help=True)
    
    parser.add_argument(
        '-p', '--useproxy',
        action="count", default=0,
        help='use proxy settings',
    )
    
    parser.add_argument(
        '-n', '--maxnumtweets',
        metavar='maxNumTweets',
        default = 10000, #curently can be 18,000 maximum, and can be upgraded to 45000 maximum
        help='set number of tweets to retrieve'
    )
    
    parser.add_argument(
        '-m', '--maxtweetsperquery',
        metavar='maxTweetsPerQuery',
        default = 100,
        help='set number of tweets per query'
    )
    
    parser.add_argument(
        '-si', '--sinceid',
        metavar='sinceId',
        default = None,
        help='set since_id to retrieve from'
    )
    
    parser.add_argument(
        '-mi', '--maxid',
        metavar='maxId',
        default = -1,
        help='set max_id to retrieve to'
    ) 
    return parser
        
if __name__ == '__main__':

     # parse arguments
    parser = get_args_parser()
    args = parser.parse_args()
    
    
    #Searched query string
    #A UTF-8, URL-encoded search query of 500 characters maximum, including operators. 
    searchedQuery = "#FedEx OR #UPS OR #DHL OR #USPS OR @FedEx OR @UPS OR @DHL OR @USPS"
    
    #maximum number of tweets to be collected
    maxNumTweets = int(args.maxnumtweets)
    
    #maximum number of tweets per are allowed to query, current maxium value is 100
    maxTweetsPerQuery = int(args.maxtweetsperquery)
    
    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = args.sinceid
    
    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    maxId = args.maxid
    
    # Could update to appplication-only auth in future
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    
    api = tweepy.API(auth, 
                     wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    if args.useproxy > 0:
        api = tweepy.API(auth, 
                         wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True,
                         proxy = 'https://internet.proxy.fedex.com:3128' )
    
    #initialize current tweets retrieved
    retriedTweetCount = 0
    print("Downloading max {0} tweets...".format(maxNumTweets))
    
    #open the saved file
    with open(SAVED_FILE_PATH, 'w') as file:
        while retriedTweetCount < maxNumTweets:
            try:
                # if did not defined a max_id
                if(maxId < 0):
                    # if did not defined a since_id
                    if(not sinceId):
                        new_tweets = api.search(q=searchedQuery, lang = 'en', count=maxTweetsPerQuery)
                    else:
                        new_tweets = api.search(q=searchedQuery, lang = 'en', count=maxTweetsPerQuery,
                                                since_id=sinceId)
                else:
                    if(not sinceId):
                        new_tweets = api.search(q=searchedQuery, lang = 'en', count=maxTweetsPerQuery,
                                                max_id=str(maxId-1))
                    else:
                        new_tweets = api.search(q=searchedQuery, lang = 'en', count=maxTweetsPerQuery,
                                                since_id=sinceId, max_id=str(maxId-1))
                
                # if cannot find any more new tweets
                if(not new_tweets):
                    print("No more tweets can be found")
                    break
                
                # if find some more new tweets, write each of them into the save file
                for tweet in new_tweets:
                    file.write(json.dumps(tweet._json) + "\r\n")
                    
                # update the current maxId to the last new
                # NOTE: the new_tweets are in reverse order of the posted timestamp
                maxId = new_tweets[-1].id
                
                # update retrieved tweets
                retriedTweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(retriedTweetCount))
            except tweepy.TweepError as err:
                print(str(err))
                break
                    
    print ("Finished Download {0} tweets and saved to {1}".format(retriedTweetCount, SAVED_FILE_PATH))

    

