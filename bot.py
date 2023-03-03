#!/usr/bin/env python

import tweepy
import os
import sys
import time 
from credentials import * 
from config import QUERY, FOLLOW, LIKE, SLEEP_TIME
  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

QUERY = '#AiArtCommunity'
MAX_TWEETS = 20
LIKE = True
FOLLOW = True
RETWEET = True
SLEEP_TIME = 60
  
print("Twitter bot which retweets, like tweets and follow users")
print("Bot Settings")
print("Like Tweets :", LIKE)
print("Follow users :", FOLLOW)

tweet_count = 0  
hashtags = ['#AiArtCommunity', '#AiiA', '#AiLust', '#YUGE', '#AiAnarchy']

for hashtag in hashtags:
    QUERY = hashtag
    tweet_count = 0
    print(f"Searching {hashtag}")
    for tweet in tweepy.Cursor(api.search_tweets, q=QUERY).items():
        try:
            print('\nTweet by: @' + tweet.user.screen_name)

            # Favorite the tweet
            if LIKE:
                tweet.favorite()
                print('Favorited the tweet')
           
        # Retweet the tweet if it has over 20 likes
            if RETWEET and tweet.favorite_count > 20:
                   tweet.retweet()
                   print('Retweeted the tweet')

            # Follow the user who tweeted
            # check that bot is not already following the user
            if FOLLOW:
                if not tweet.user.following:
                    tweet.user.follow()
                    print('Followed the user')

            tweet_count += 1
            if tweet_count == MAX_TWEETS:
                print(f"Searching {hashtag}")
                tweet_count = 0
                break

            time.sleep(SLEEP_TIME)

        except tweepy.errors.Forbidden as e:
            if "already favorited this status" in str(e):
                print("Already liked this tweet. Skipping...")
            else:
                print("Error:", e)
            continue




