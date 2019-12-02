import json
import oauth2 as oauth
import tweepy
import cfg
import threading
import requests
import urllib2
from requests.auth import HTTPBasicAuth
import sys

auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)

api = tweepy.API(auth)

#apex validation
headers = {'TRN-Api-Key': '3c0a15fd-ac7c-4f37-9f7a-47bd7a76286d'}

#setup retrieve mentions
consumer = oauth.Consumer(key=cfg.consumer_key, secret=cfg.consumer_secret)
access_token = oauth.Token(key=cfg.access_token, secret=cfg.access_token_secret)
client = oauth.Client(consumer, access_token)

twitter_endpoint = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json?screen_name=ApexLegendsBot'

twitter_response, twitter_data = client.request(twitter_endpoint)

#access API to get mentions
tweets = json.loads(twitter_data) 

last_id = tweets[0]['id']
print 'The most recent mention tweet ID is: '+str(last_id)

    