# -*- coding: utf-8 -*-

"""
Created on Mon Jul 24 11:47:29 2017

A scripts using Python library tweepy to connect to Twitter Streaming API 
and download data.

Command to run: python stream.py -p -j -n 1000 
@author: 5004756 Lei Feng
"""
# Import neccesary methods from tweepy library
import tweepy
import json
import argparse
import sys

# Constant variables of user credentials to access Twitter API
# all information from "https://apps.twitter.com/app/14056047/keys" - CustomerVoiceListener
CONSUMER_KEY = "9tM7BBlEX38HoSsMEKMpyVc1b"# os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = "sFhHfvcwkYJTan0CKmj7l78B1FsRgjrm0GfUrI6UCVagI1hKSH"#os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_TOKEN = "770679954-yJWgA3ZuHF9nZfjffN35HyhnHfWsIOuYbAFhnFNr"#os.environ['TWITTER_ACCESS_KEY']
ACCESS_SECRET = "9H2mH56XiJAnvYfzBbtR3oEGcnbeghQj6vVmM7fYSmzK0"#os.environ['TWITTER_ACCESS_SECRET']
SAVED_FILE_PATH = "./data/stream_data.txt"



class EchoStreamListener(tweepy.StreamListener):
    def __init__(self, api, dump_json=False, numtweets=0):
        self.api = api
        self.dump_json = dump_json
        self.count = 0
        self.limit = int(numtweets)
        super(tweepy.StreamListener, self).__init__()

    def on_data(self, tweet):
        tweet_data = json.loads(tweet)
        if 'text' in tweet_data:
            savefile = open(SAVED_FILE_PATH, 'a')
            if self.dump_json:
                print(tweet.rstrip() + "\r\n")
#                print(json.dumps(tweet_data) + "\r\n")
                savefile.write(tweet.rstrip())
                savefile.write("\r\n")                
            else:
                print(tweet_data['text'].encode("utf-8").rstrip())
                savefile.write(tweet_data['text'].encode("utf-8").rstrip())
                savefile.write("\r\n")             
            savefile.close()   
            self.count = self.count + 1
            print("collected " + str(self.count) + " tweets.")
            return False if self.count == self.limit else True
     
           
    def on_error(self, status_code):
        #If clients exceed a limited number of attempts to 
        # connect to the streaming API in a window of time
        # it is essential to stop further connection attempts 
        # for a few minutes if a HTTP 420 response is received. 
        # If your client is rate limited frequently, 
        # it is possible that your IP will be blocked from accessing Twitter for an indeterminate period of time.
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
        return True

    def on_timeout(self):
        return True


def get_args_parser():
    '''A function parse the arguments'''
    parser = argparse.ArgumentParser(add_help=True)
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-j', '--json',
        action='store_true',
        help='dump each tweet as a json string'
    )
    group.add_argument(
        '-t', '--text',
        dest='json',
        action='store_false',
        help='dump each tweet\'s text'
    )
    

    parser.add_argument(
        '-p', '--useproxy',
        action="count", default=0,
        help='use proxy settings',
    )
    
    parser.add_argument(
        '-n', '--numtweets',
        metavar='numtweets',
        default = sys.maxsize,
        help='set number of tweets to retrieve'
    )

    return parser


class ProxyStream(tweepy.Stream):
    '''A new strem class with proxy settings though define a new session'''
    def new_session(self):
        super().new_session() # PY2: super(ProxyStream, self).new_session()
        self.session.proxies = {
            'https': 'https://internet.proxy.fedex.com:3128',
            'http': 'http://internet.proxy.fedex.com:3128'
        }


# main funciton
if __name__ == '__main__':
    # parse arguments
    parser = get_args_parser()
    args = parser.parse_args()

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    myapi = tweepy.API(auth,
                       wait_on_rate_limit=True,
                       wait_on_rate_limit_notify=True)
    
    listener = EchoStreamListener(api = myapi, dump_json=args.json, numtweets=args.numtweets)
    
    stream = tweepy.streaming.Stream(auth, listener)
    if args.useproxy > 0:
        stream = ProxyStream(auth, listener)
        
    #This line filter Twitter Streams to capture data by hashtags:
    # ['#FedEx', '#UPS', '#DHL', '#USPS', '@FedEx', '@UPS', '@DHL', '@USPS']
    stream.filter(track=['#FedEx', '#UPS', '#DHL', '#USPS', '@FedEx', '@UPS', '@DHL', '@USPS'], languages=["en"])


        
