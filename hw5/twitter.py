 # -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 14:03:44 2014

@author: mborges, mkeene & hpelletier
"""

from pattern.web import *
from pattern.en import *
import enchant
import re

def get_tweets(query,num):
    """Searches Twitter for the given query and returns a list of the specified 
       number of tweets that come up as results.
       Inputs: query: the term searched for on Twitter
               num: the number of related tweets to return
       Outputs: a list of tweets (of length num) related to query
    """
    tweet_list = Twitter().search(query,count=num,cached=False)
    Tweets = []
    for tweet in tweet_list:
        Tweets.append(tweet.text)
    return Tweets                     
    
def filter_tweet(tweet):
    """Removes mentions, tags, links, 'RT's, non-english words, and single
       letters from 'raw' tweets and returns lowercase 'filtered' tweets.
       Input: raw tweet
       Output: filtered tweet"""
        
    letter_list = ['b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    d = enchant.Dict("en_US")
    word_list = re.findall(r"[a-zA-Z'#@]+",tweet)
    new_list = []
    for word in word_list:  
        word = word.lower()
        if word.find('#')==-1 and word.find('rt')==-1 and word.find('@')==-1 and word.find('http://')==-1 and d.check(word) == True and word not in letter_list:                       
            new_list.append(word)                 
    return ' '.join(new_list)
    
def get_avg_sentiment(sent_list):
    """For a list of sentiments, removes trivial entries
        (0.0, 0.0) and returns the average sentiment.
        Input: a list of sentiments
        Output: the average sentiment"""

    new_list = []
    for sent in sent_list:
        if sent[0]!=0.0 and sent[1]!=0.0:
            new_list.append(sent)
            
    polarity = []
    subjectivity = []
    for sent in new_list:
        polarity.append(sent[0])
        subjectivity.append(sent[1])
        
    total_pol = 0
    for i in range(len(polarity)):
        total_pol += polarity[i]
    avg_pol = total_pol/len(polarity)
    
    total_subj = 0
    for i in range(len(subjectivity)):
        total_subj += subjectivity[i]
    avg_subj = total_subj/len(subjectivity)      
    
    return (avg_pol,avg_subj)    
       
def MAIN(query,num):
    """Searches Twitter for the given query and uses num tweets
       that come up as results to determine the overall sentiment 
       of the query on twitter at any given moment.
       Inputs: query: the term searched for on twitter
               num: number of related tweets to use
       Output: the average sentiment
    """
    Tweets = get_tweets(query,num)    
    filtered_tweets = []
    for tweet in Tweets:
        filtered_tweets.append(filter_tweet(tweet))
    sentiment_list = []
    for tweet in filtered_tweets:
        sentiment_list.append(sentiment(tweet))
    return get_avg_sentiment(sentiment_list)
    
print MAIN('oscars',50)