# -*- coding: utf-8 -*-
"""
Created on Sun Mar  2 17:06:47 2014

@author: hpelletier
"""

import numpy as np
import matplotlib.pyplot as plt

def make_graph(data1,data2,hashtag1,hashtag2):
    """Visualizes the sentiment analysis of two hashtags and graphs the components in comparison
        to one another"""
    #sets number of groups we will be comparing
    n_groups = 2
    
    d1 = data1 #data from hashtag 1
    d2 = data2
    h1 = str(hashtag1)
    h2 = str(hashtag2)

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.9
    #error_config = {'ecolor': '0.3'}


    rects1 = plt.bar(index, data1, bar_width,
                 alpha=opacity,
                 color='b',
                 label= h1)


    rects2 = plt.bar(index + bar_width, data2, bar_width,
                 alpha=opacity,
                 color='g',
                 label= h2)
                 
    plt.ylim([-1.5,1.5])
    plt.xlabel('Criteria')
    plt.ylabel('Scores')
    plt.title('Positivity and Subjectivity by Hashtag')
    plt.xticks(index + bar_width, ('Positivity', 'Subjectivity'))
    plt.legend()

    plt.tight_layout()
    plt.show()
