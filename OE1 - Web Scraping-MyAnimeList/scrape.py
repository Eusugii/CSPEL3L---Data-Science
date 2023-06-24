#Scraping data from Twitter & on a web page
#tweepy, csv, 
import tweepy
import twitter
import csv
from datetime import datetime

#Setup Twitter API credentials
cons_key = 'UaaoslQ7UkS9oGZB3Hm4fBgJQ'
cons_secret = '2UEByLLeve4dt5hqdoB3xDCACaJx1sl7yJWxYY44f9vZTWp64z'
access_token = '1107229751918256129-Xma4H2QLaqw6crNh3H9mL8nyRULhqy'
access_token_secret = 'CRkdwMt2ZtyM6qcftD8APu5bkKTVnqzgJFwJNYVaiNuyv'

#Authentication of twitter API
auth = tweepy.OAuth2UserHandler(cons_key,cons_secret,)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

api = twitter.Api(consumer_key=cons_key,consumer_secret=cons_secret,access_token_key=access_token,access_token_secret=access_token_secret)

#Specify the search query and date range
search_string = 'oceangate'
startdate = datetime(2023,6,10)
enddate = datetime(2023,6,24)

#Convert date to desired format
start_date_fmt = startdate.strftime('&Y-%m-%d')
end_date_fmt = enddate.strftime('&Y-%m-%d')

#Set the number of tweets to scrape
tweet_counts = 10

#Scrape from Twitter
tweets = tweepy.Cursor(api.search_tweets,q=search_string,lang='en',tweet_mode='extended', since=start_date_fmt,until=end_date_fmt).items(tweet_counts)

#Create CSV file
csv_file = open('scraped_data.csv','w',newline='',encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Text','Author','Created At'])

for tweet in tweets:
    text=tweet.full_text
    author = tweet.author.screen_name
    created_at = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
    csv_writer.writerow(text,author,created_at)

csv_file.close()

