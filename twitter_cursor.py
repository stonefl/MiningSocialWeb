

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 11:47:29 2017

A test scripts using Python library tweepy to connect to Twitter Search API 
and download data.

https://dev.twitter.com/rest/reference/get/search/tweets

@author: 5004756
"""

# Import neccesary methods from tweepy library
import tweepy
import json


# Global variables of user credentials to access Twitter API
# all information from "https://apps.twitter.com/app/13083667/keys" -LeiFengBlog
CONSUMER_KEY = "q1BbMVgJGpPZ3IVrCkmv1tcix"
CONSUMER_SECRET = "sfwpBjHPijxbjTBDyiOmFb5MxcGa3LaXUpim1NmbA1gWFfzVjK"
ACCESS_KEY = "770679954-vWDVGhFKOdwR1vzN56Cgcc2Rcf4QoGhCBPwOvcgd"
ACCESS_SECRET = "VKmuoM3wLDwT8QrOhyzE9ySIsZQnnEp4FSRGdXVLbTLSl"
SAVED_FILE_PATH = "./data/search_data.json"

        
if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    
    # Could up to appplication-only auth in future
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, proxy='https://internet.proxy.fedex.com:3128' )
    
    query = "#FedEx OR #UPS OR #DHL OR #USPS"
    search_results = api.search(q=query, result_type = 'mixed', lang = 'en', count=102)
    
    i = 0
    savefile = open(SAVED_FILE_PATH, 'a')
    for tweet in search_results:
        i = i + 1
        print("tweet " + str(i) + ":")
        print(json.dumps(tweet._json))
        savefile.write(json.dumps(tweet._json) + "\r\n")
        
    savefile.close()
    

