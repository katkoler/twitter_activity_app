#!/usr/bin/env python2
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import config
import os
from io import open


#Twitter API credentials
consumer_key = os.environ["twitter_consumer_key"] 
consumer_secret = os.environ["twitter_consumer_secret"] 
access_token = os.environ["twitter_access_token"] 
access_token_secret = os.environ["twitter_access_token_secret"]


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	# with open('%s_tweets.csv' % screen_name, 'wb') as f:
	with open('%s_tweets.csv' % screen_name, 'w', newline='', encoding='utf-8-sig') as f:
		writer = csv.writer(f)
		writer.writerow([u"id",u"created_at",u"text"])
		writer.writerows(outtweets)
	# # write the csv 
	# with open('%s_tweets.csv' % screen_name, 'wb') as f:
	# 	writer = csv.writer(f) 
	# 	a_new = [tuple(map(str, i)) for i in outtweets]
	# 	writer.writerow([str.encode("id"),str.encode("created_at"),str.encode("text"),str.encode("media_url")])
	# 	writer.writerows(str.encode(a_new))

	pass


if __name__ == "__main__":
	#pass in the username of the account you want to download
	get_all_tweets("katkoler")

# get_all_tweets("katkoler")



