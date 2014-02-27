 # -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 14:03:44 2014

@author: mborges & hpelletier
"""

from pattern.web import *
from pattern.en import *
import enchant
import re

def get_trends():
    Trends = Twitter().trends()

def get_trending_tweets(Trends):
    L = []
    for trend in Trends:
        s = Twitter().stream(trend)
        for i in range(10):
            #time.sleep(1)
            s.update(bytes=1024)
            L.append(plaintext(s[-1].text)) if s else ''
            print (plaintext(s[-1].text)) if s else ''
            
def sentiment_analysis(L):   
    for i in range(len(L)):
        print sentiment(L[i])
        
tweet = "RT @Tweet This is a tweet! #tweet"
    
def filter_tweet(tweet):
    d = enchant.Dict("en_US")
    tweet_list = re.findall(r"[a-zA-z'#@]+",tweet)
    for tweet in tweet_list:
        if tweet.find('#') > -1 or tweet == 'RT' or tweet.find('@') > -1:
            tweet_list.remove(tweet)
    for tweet in tweet_list:
        if tweet.find('#') > -1 or tweet == 'RT' or tweet.find('@') > -1:
            tweet_list.remove(tweet)            
    for tweet in tweet_list:        
        if d.check(tweet) == False:
            tweet_list.remove(tweet)
    tweet_string = ' '.join(tweet_list)             
    return tweet_string
    
print filter_tweet(tweet)