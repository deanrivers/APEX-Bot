import json
import oauth2 as oauth
import tweepy
import cfg
import threading
import time
import requests
import urllib2
from requests.auth import HTTPBasicAuth
import datetime
import sys
import process

#initial process
process.newProcess()

print 'Starting Loop in 60s'
#ongoing process
while(1>0):
    time.sleep(60)
    process.newProcess()
    print 'Restarting Loop in 60s'
    print ''
    
