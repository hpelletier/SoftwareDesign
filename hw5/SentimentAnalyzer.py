# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 19:59:26 2014

@author: mborges, mkeene, hpelletier
"""

import numpy as np
import matplotlib.pyplot as plt
import Tkinter
from Tkinter import *
import ttk
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
       letters (excl. 'a' and 'i') from 'raw' tweets and returns lowercase 
       'filtered' tweets.
       Input: raw tweet
       Output: filtered tweet
    """        
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
       Output: the average sentiment
    """
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
       
def analyze_sentiment(query,num):
    """Searches Twitter for the given query and uses the first num tweets
       that come up as results to determine the overall sentiment 
       of the query on twitter at any given moment
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
    
def make_graph(data1,data2,query1,query2):
    """Visualizes the sentiment analysis of two queries by graphing the 
       components of each in comparison to one another
       Inputs: data1: the avg sentiment of the first query's tweets
               data2: the avg sentiment of the second query's tweets
               query1: the first query entered by the user
               query2: the second query entered by the user
       Output: a graph visualizing the sentiment anaylsis data
    """
    #sets number of queries we will be comparing
    n_groups = 2
    
    d1 = data1 #data from query 1
    d2 = data2
    q1 = str(query1)
    q2 = str(query2)

    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.9
    
    rects1 = plt.bar(index, data1, bar_width,
                 alpha=opacity,
                 color='b',
                 label= q1)

    rects2 = plt.bar(index + bar_width, data2, bar_width,
                 alpha=opacity,
                 color='g',
                 label= q2)
                 
    plt.ylim([-1.5,1.5])
    plt.xlabel('Criteria')
    plt.ylabel('Scores')
    plt.title('Positivity and Subjectivity by Query')
    plt.xticks(index + bar_width, ('Positivity', 'Subjectivity'))
    plt.legend()
    plt.tight_layout()    
    plt.show()    

def on_ok():
    """Called when the 'OK' button of the GUI is pressed
       Takes the user input from the GUI and uses it to create the 
       graphical representation of the data
    """
    query1=E1.get()
    query2=E2.get()
    number=E3.get()
    data1=analyze_sentiment(query1,number)
    data2=analyze_sentiment(query2,number)
    make_graph(data1,data2,query1,query2)
    

"""Creates the GUI and defines what happens when its buttons are pressed
"""    
root = Tkinter.Tk()
root.title('Sentiment Test')
root.configure(background='white')

label1=Label(text='What queries would you like to compare? (ex. #fail, oscars)',background='white',foreground='gray38').pack(side=TOP,padx=10,pady=10)
E1=Entry(root,width=10)
E1.pack(side=TOP,padx=10,pady=10)

label2=Label(text='And what is the other one?',background='white',foreground='gray38').pack(side=TOP,padx=10,pady=10)
E2=Entry(root,width=10)
E2.pack(side=TOP,padx=10,pady=10)

label3=Label(text='How many tweets should be used to determine the sentiment?',background='white',foreground='gray38').pack(side=TOP,padx=10,pady=10)
E3=Entry(root,width=10)
E3.pack(side=TOP,padx=10,pady=10)

    
ttk.Style().configure('TButton',padding=6,relief='flat',background='white')

ttk.Button(root,text='OK',command=on_ok).pack(side=LEFT)
ttk.Button(root,text='CLOSE',command=root.quit).pack(side=RIGHT)

root.mainloop()

