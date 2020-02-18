##########scrape player's performance data from transfermarkt, 10 leagues in total


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

#### set file name
file_name = 'data_1.csv'

##### England, Italy, Spain, Germany, France. Tier 1 and 2 leagues in each country
#url='https://www.transfermarkt.us/premier-league/startseite/wettbewerb/GB2'
#url = 'https://www.transfermarkt.com/serie-a/startseite/wettbewerb/IT2'
#url = 'https://www.transfermarkt.com/primera-division/startseite/wettbewerb/ES2'
#url = 'https://www.transfermarkt.com/1-bundesliga/startseite/wettbewerb/L2'
url = 'https://www.transfermarkt.com/ligue-1/startseite/wettbewerb/FR2'

#### define function that get the text of website
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
def get_page(url):
    responce = requests.get(url,headers=headers)
    soup = BeautifulSoup(responce.text,'lxml')
    return soup

#### get team links in each league   
def get_team_links(link_url):  
    soup=get_page(link_url)
    links_div=soup.find_all('td', class_= "hauptlink no-border-links hide-for-small hide-for-pad")
    links = [td.a.get('href') for td in links_div]
    
    return links
    
#### get player links in each team    
def get_player_links(link_url):  
    soup=get_page(link_url)
    links_div=soup.find_all('div', class_="di nowrap")
    links = [div.a.get('href') for div in links_div]
    
    return links
    
#### get player info
def get_player_info(url):
    info = {}
    soup = get_page(url)
    tp1 = soup.find_all('h1', itemprop="name")
    name =tp1[0].text if tp1 else 'NaN'
    info['name'] = name 
    #number of trophies
    tr = soup.find_all('span', class_="dataErfolgAnzahl")
    trophy = 0
    for i in range(len(tr)):
        trophy = trophy + int(tr[i].text)
    info['trophy'] = trophy if tr else 'NaN'
    #country
    tp2 = soup.find_all('span', itemprop="nationality")
    nationality = tp2[0].text if tp2 else 'NaN'
    info['nationality'] = nationality 
    #height
    tp3 = soup.find_all('span', itemprop="height")
    height = tp3[0].text if tp3 else 'NaN'
    info['height'] = height 
    
    ##injury 
    injury_info = soup.find_all('div', class_="verletzungsbox")
    injury = injury_info[0].text.replace('\n','') if injury_info else 0
    info['injury'] = injury
    
    ##start_lineup
    quote = {'startelfquote':0,'minutenquote':0,'nothing': 0}
    start_lineup = soup.find_all('div', class_="progress-pie-chart")
    for i in range(2):
        try:
            s1 = start_lineup[i]['id'] if start_lineup else 'nothing'
            quote[s1] =  start_lineup[i]['data-percent'] if start_lineup else 0
        except IndexError:
            quote[s1] = 0 if start_lineup else 0
    info['startelfquote'] = quote['startelfquote']
    info['minutenquote'] = quote['minutenquote']
    ##table data
    table_data = soup.find_all('table', class_="auflistung")
    table = {}
    for tr in table_data[0].find_all('tr'):
        for th in tr.find_all('th'):
            for td in tr.find_all('td'):
                table[th.text] = td.text
                temp1 = td.find_all(title="Twitter")
                twitter = temp1[0].get('href') if temp1 else 'NaN'
                info['twitter'] = twitter
#                 temp2 = td.find_all(title="Instagram")
#                 instagram = temp2[0].get('href') if temp2 else 'NaN'
#                 info['instagram'] = instagram
                
    REPLACE_BY_SPACE_RE = re.compile('\s')
    for key in table:
        table[key] = REPLACE_BY_SPACE_RE.sub('', table[key])
    info['age']  = table['Age:'] if 'Age:' in table.keys() else 'NaN'
    info['Position']  = table['Position:'] if 'Position:' in table.keys() else 'NaN'
    info['Foot']      = table['Foot:'] if 'Foot:' in table.keys() else 'NaN'
    info['Player_agent']  = table['Player agent:'] if 'Player agent:' in table.keys() else 'NaN'
    info['join_date']  = table['Joined:'] if 'Joined:' in table.keys() else 'NaN'
    info['exp_date']  = table['Contract expires:'] if 'Contract expires:' in table.keys() else 'NaN'
    info['exten_date']  = table['Date of last contract extension:'] if 'Date of last contract extension:' in table.keys() else 'NaN'
    info['outfitter']  = table['Outfitter:'] if 'Outfitter:' in table.keys() else 'NaN'    
    info['club']  = table['\n                            Current club:\n                        '] if '\n                            Current club:\n                        ' in table.keys() else 'NaN' 
    tp4 = soup.find_all('div', class_="right-td")
    market_value = tp4[0].text if tp4 else 'NaN'
    
    stats_table = soup.find_all('table', class_='items')
    header = stats_table[0].thead.find_all('th') if stats_table else []
    footer = stats_table[0].tfoot.find_all('td') if stats_table else []
    stats ={'Appearances':'0', 'Minutes played':'0', 'Goals': '0','Assists': '0','Minutes per goal': '0'}
    for i in range(len(header)):
        header_title = header[i].find_all('a')[0]
        tt = header_title.span['title'] if header_title.find_all('span') else 'NaN'

        try:
            stats[tt] = footer[i].text if footer[i] else 'NaN'
        except IndexError:
            stats[tt] = 'NaN' 

    info['appearance'] = stats['Appearances'] 
    info['minutes'] = stats['Minutes played'] 
    info['goals'] = stats['Goals'] 
    info['Assists'] = stats['Assists'] 
    info['min_per_goal'] = stats['Minutes per goal']
    
    info['market_value'] = REPLACE_BY_SPACE_RE.sub('', market_value) 
    return info



if __name__ == "__main__":
#### get each player's link  and store them in a list
    team = get_team_links(url)
    player_links = []
    for i in range(len(team)):
        time.sleep(2)
        print('scraping {}th page'.format(i) + ' of player links')
        player_links.append(get_player_links('https://www.transfermarkt.us'+ team[i]))
        
        
        
#### get each player's info  and store them in a list    
    total_player = [x for j in player_links for x in j]
    total_player_links = list(set(total_player))
    ini_info = get_player_info('https://www.transfermarkt.us'+total_player_links[0])
    df = pd.DataFrame(ini_info,index=[0])
    for i in range(1,len(total_player_links)):
        time.sleep(np.random.randint(1, 3))
        player = get_player_info('https://www.transfermarkt.us'+total_player_links[i])
        df.loc['{}'.format(i)] = player
        if i%10 == 0:
            print('scarping {}th page'.format(i) + ' of player info')
            
    df.to_csv(file_name)
    
    
