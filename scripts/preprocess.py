import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import nltk

import pycountry
import pycountry_convert as pc

    

###format player join team date into year
def date_change(x):
    date_input = x if '20' in x else 0
    try:
        ndays = (datetime.datetime.strptime(date_input , "%d.%m.%Y").date() - datetime.datetime.strptime("Dec31,2019", "%b%d,%Y").date()).days
    except:
        ndays = 0
    return ndays/365
    
###format join twitter date into year   
def date_change_twitter(x):
    date_input = x if '20' in x else 0
    try:
        ndays = (datetime.datetime.strptime("Dec31,2019", "%b%d,%Y").date() - datetime.datetime.strptime(date_input, "%I:%M%d%b%Y").date()).days
    except:
        ndays = 0
    return ndays/365

###market value, make units consistent
def value_trans(value):
    try:
        if 'm' in value:
            v = value.replace('$','').replace('m', '') 
        elif 'k' in value:
            v = float(value.replace('$','').replace('k', ''))/1000
    except:
        v = 0
    return float(v)
###identify the continent for each player    
def country_to_continent(country_name):
    try:
        if country_name == 'DR Congo':
            country_continent_name = 'Africa'
        else:
            fuzzy = pycountry.countries.search_fuzzy(country_name)
            country_alpha2 = pc.country_name_to_country_alpha2(fuzzy[0].name)
            country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
            country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    except:
        country_continent_name = 'Europe'
    return country_continent_name

###reduce category of position

def position(info):
    if 'Forward' in info:
        info = 'Forward'
    elif 'Midfielder' in info:
        info = 'Midfielder'
    elif 'Defender' in info:
        info = 'Defender'
    elif 'Goalkeeper' in info:
        info = 'Goalkeeper'
    return info



if __name__ == "__main__":



    #### Load Data
    df = pd.read_csv('final.csv')


    #### remove data that has null values
    df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0.1', 'joint_tweets','fullname','id','lists'])
    df = df.drop(df.index[[336]])####drop row

    data_train = df[df['twitter'].notnull()]
    data_train = data_train[data_train['followers'].notnull()]
    data_train = data_train[data_train['market_value'].notna()]
    data_train.index = range(len(data_train))
    
    #### process height feature
    data_train['height_ver2'] = data_train['height'].apply(lambda x: str(x).replace(',', '').replace('m', ''))
    
    #### format contract start date into years
    data_train['join_date_ver1'] = data_train['join_date'].apply(lambda x: x if '20' in x else 0)####20 year
    data_train['join_date_ver2'] = data_train['join_date_ver1'].apply(lambda x: (datetime.datetime.strptime("Dec31,2019", "%b%d,%Y").date() - \
                                                                datetime.datetime.strptime(x, "%b%d,%Y").date()).days/365 if x!=0  else 0)
    #### format contract end date    
    data_train['exp_date_ver2'] = data_train['exp_date'].apply(date_change)
    #### format joined twitter date
    data_train['date_joined_twitter_ver2'] = data_train['date_joined'].apply(date_change_twitter)
    
    
    #### number of thopies
    data_train['trophy_ver2'] = data_train['trophy'].apply(lambda x: 0 if np.isnan(float(x)) else x)
    
    #### player agent into binary 
    data_train['Player_agent_ver2'] = data_train['Player_agent'].apply(lambda x : 0 if (x =='Relatives')|(x =='noagent ')|(x =='notclarified') else 1)
    
    #### format sentiment score : score and length of tweet
    data_train['sent_score'] = data_train['sent_mean']*data_train['sent_length']
    
    #### reduce category of position
    data_train['position_ver2'] = data_train['Position'].apply(position )

    #### left or right foot
    data_train['Foot_ver2'] = data_train['Foot'].apply(lambda x : x if (x == 'left')|(x == 'right') else 'both')
    
    #### adidas or nike
    data_train['outfitter_ver2'] = data_train['outfitter'].apply(lambda x : x if (x == 'Nike')|(x == 'adidas') else 'other')
    
    #### identify the continent for each player
    data_train['nationality_ver2'] = data_train['nationality'].apply(country_to_continent)
    
    #### market value, make units consistent
    data_train['market_value_ver2'] = data_train['market_value'].apply(value_trans)
    
    #### format twitter features
    data_train['num_tweets_ver2'] = data_train['num_tweets'].apply(lambda x: float(0) if (x == '-')|(x == 'NaN') else float(x))
    data_train['following_ver2'] = data_train['following'].apply(lambda x: float(0) if (x == '-')|(x == 'NaN') else float(x))
    data_train['followers_ver2'] = data_train['followers'].apply(lambda x: float(0) if (x == '-')|(x == 'NaN') else float(x))
    data_train['likes_ver2'] = data_train['likes'].apply(lambda x: float(0) if (x == '-')|(x == 'NaN') else float(x))
    data_train['date_joined_twitter_ver3'] = data_train['date_joined_twitter_ver2'].apply(lambda x: float(0) if (x == '-')|(x == 'NaN') else float(x))    
        
    #### performance features that have missing value as 0
    data_train['appearance_ver2'] = data_train['appearance'].apply(lambda x: float(0) if (x == '-')|(x == 'NaN') else float(x))
    data_train['minutes_ver2'] = data_train['minutes'].apply(lambda x: float(0) if (x == '-')|(x == 'NaN') else float(x))
    data_train['goals_ver2'] = data_train['goals'].apply(lambda x : x if x!='-' else 0)
    data_train['Assists_ver2'] = data_train['Assists'].apply(lambda x : x if x!='-' else 0)
    data_train['min_per_goal_ver2'] = data_train['min_per_goal'].apply(lambda x : x if x!='-' else 0)
    data_train['injury_ver2'] = data_train['injury'].apply(lambda x : 0 if x=='0' else 1)
    
    #### impute missing values
   
    imputer = IterativeImputer(max_iter=10, random_state=0)
    duty_data = data_train[['height_ver2', 'join_date_ver2', 'exp_date_ver2', 'sent_score', 'sent_max', 'sent_min', 'best', 'goal', 'good', 'great', 'love']] 
    imputed_data= imputer.fit_transform(duty_data)
    imp =imputer.fit_transform(duty_data)
    imp_data = pd.DataFrame(imp, columns=['height_ver2', 'join_date_ver2', 'exp_date_ver2', 'sent_score', 'sent_max', 'sent_min', 'best', 'goal', 'good', 'great', 'love'])
    
    #### one hot encoding features
    dummies_foot = pd.get_dummies(data_train['Foot_ver2'], prefix= 'foot')
    dummies_position = pd.get_dummies(data_train['position_ver2'], prefix= 'position')
    dummies_outfitter = pd.get_dummies(data_train['outfitter_ver2'], prefix= 'outfitter')
    dummies_nationality = pd.get_dummies(data_train['nationality_ver2'], prefix='nationality_ver2')
    
    ###pick data that dont need impute or dummies
    part1 = data_train[['age', 'injury_ver2','startelfquote', 'minutenquote','Player_agent_ver2', 'appearance_ver2', 'minutes_ver2',\
                        'num_tweets_ver2', 'following_ver2', 'followers_ver2', 'likes_ver2',\
                        'date_joined_twitter_ver3', 'goals_ver2', 'Assists_ver2', 'min_per_goal_ver2', 'market_value_ver2' ]]
                        
    final = pd.concat([imp_data, dummies_foot,dummies_position,dummies_outfitter,dummies_nationality, part1],axis=1)
    
    final.to_csv('final0217_orig.csv')
    
    
    
    
    