import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import string
import nltk

from twitterscraper.query import query_user_info
from twitterscraper import query_tweets

def get_user_info(twitter_user):
    """
    An example of using the query_user_info method
    :param twitter_user: the twitter user to capture user data
    :return: twitter_user_data: returns a dictionary of twitter user data
    """
    userinfo = query_user_info(user= twitter_user)
    twitter_user_data = {"user":0, "fullname":0, "date_joined":0, "id":0, "num_tweets":0, "following":0, "followers":0, "likes":0, "lists":0}
    twitter_user_data["user"] = userinfo.user if userinfo else 0
    twitter_user_data["fullname"] = userinfo.full_name if userinfo else 0
    twitter_user_data["date_joined"] = userinfo.date_joined if userinfo else 0
    twitter_user_data["id"] = userinfo.id if userinfo else 0
    twitter_user_data["num_tweets"] = userinfo.tweets if userinfo else 0
    twitter_user_data["following"] = userinfo.following if userinfo else 0
    twitter_user_data["followers"] = userinfo.followers if userinfo else 0
    twitter_user_data["likes"] = userinfo.likes if userinfo else 0
    
    return twitter_user_data
    
    
if __name__ == "__main__":

    for i in range(1,11):
        locals()['df'+str(i)]=pd.read_csv('data_126_{}.csv'.format(i))
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7 ,df8 ,df9, df10], ignore_index=True)

####process the twitter account name
    follow = df[df['twitter'].notnull()]
    twit = follow[['name', 'twitter']]
    link = follow['twitter'].values.tolist()
    link_list = [link[i].replace('http://twitter.com/', '') for i in range(len(link))]
    account = twit['twitter'].apply(lambda x: str(x).replace('http://twitter.com/', '').replace('http://www.twitter.com/', '').replace('http://https:twitter.co', '').replace('http:// twitter.com/', ''))
    print(account)
    twit.loc[:,'account'] = account.values.tolist()

    twit.index = range(len(twit))
####init the tweets csv file   
    first = get_user_info(link_list[0])
    first['name2'] =  twit.name.loc[0]
    dt = pd.DataFrame(first,index=[0])
    
####scrape the tweets   
    for i in range(len(twit):
        player_twitter = get_user_info(link_list[i])
        player_twitter['name2'] = twit.name.loc[i]
        begin_date = datetime.datetime.strptime("Dec 15 2019", "%b %d %Y").date()
        tweets = query_tweets(player_twitter['user'], lang = 'en', limit = 1, begindate=begin_date)
        tw = []
        for tweet in tweets:
            tw.append(tweet.text)
            alltweets = ' '.join(tw)
        player_twitter['tweets'] = alltweets
            
        dt.loc['{}'.format(i)] = player_twitter
        if i%2 == 0:
            print('scarping {}th page'.format(i))
    
    dt.to_csv('tweets.csv')