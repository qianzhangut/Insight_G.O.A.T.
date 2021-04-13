# G.O.A.T. – Greatest of All Time!
Find your G.O.A.T. player!

## Summary
[G.O.A.T.](http://datafuture.me/) is a multifunctional website that uses player performance data and twitter information to estimate their market values for the current season (19/20) in European leagues. 

## Use case
Football is the most popular sport in the world. In 2019, clubs around the world completed 18,042 international transfers. The total value of international transfers reached USD 7.35 billion. From a managerial perspective, the most important decisions that team managers make concern player transfers, which is related to player's market value. It plays an important role in the transfer negotiations. These values have traditionally been estimated by football experts. This product provides a data driven solution for forecasting player's market value so that team managers can make better decisions when signing new players.

## Data Collection
Data is collected by web scraping from [transfermarkt](https://www.transfermarkt.com/) and [twitter](https://twitter.com/):

- transfermarkt: player performance data
- twitter: number of followers, likes, tweets, and tweets of hashtags of each player's name

I used Python request, BeautifulSoup, selenium, and json libraries to scrape and parse the html and json data.

## Exploratory Analysis
### EDA
<p align="center"><img src="https://github.com/qianzhangut/qian_insight/blob/master/img/output3.png" width="500"/></p>
Forward and midfield are more expensive than defender and goalkeeper.


<p align="center"><img src="https://github.com/qianzhangut/qian_insight/blob/master/img/output5.png" width="500"/></p>
European and and South American players are more popular in social media.

### Data Processing
- Selected players performance data such as number of matches played, number of goals and assists, position, injury, contract length, etc.
- Cleaned the tweets, including removing links, punctuation and stopwords, as well as lemmatization
- Obtained the sentiment score of each player based on the tweets. Built a TF-IDF matrix with all tweets and extracted a few columns, which represent words such 'good', 'great', 'goal', etc. 

## Models
Random forest regressions were used to predict players' market value. Datasets were split 80% and 20% into train and test datasets respectively. Hyperparameter tuning was performed using Bayesian optimizaiton with 5-fold cross validation to obtain the optimized parameters for the model. Evaluations of the model performances were subsequently performed on the test dataset using several metrics including mean squared error, mean absolute error and R2.


## Web Application
A web app was built with Flask and hosted on AWS that allows users to predict soccer players' value based on the performance data and social media information. Player's information and a wordcloud generated from the tweet are displayed. Click [here](http://datafuture.me/) to access the website.




