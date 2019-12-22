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
import mailer

#setup
#twitter validation
auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)
api = tweepy.API(auth)

#apex API key
headers = cfg.headers

#setup credentials to access Twitter mentions via API
consumer = oauth.Consumer(key=cfg.consumer_key, secret=cfg.consumer_secret)
access_token = oauth.Token(key=cfg.access_token, secret=cfg.access_token_secret)
client = oauth.Client(consumer, access_token)

#write last since_id to since_ids.txt
def updateSinceIDs(tweetID):
    f = open("since_ids.txt", "a")
    f.write(str(tweetID) + "\n") 
    f.close()
    print '"since_ids.txt" Update triggered for: ' + str(tweetID)
    return True

#retrieve last since_id
def retrieveLastID():
    #update since_id to the last line on initial call
    fileHandle = open ( 'since_ids.txt',"r" )
    lineList = fileHandle.readlines()
    fileHandle.close()
    print "The last line value in the since_ids.txt is: "
    #print lineList[len(lineList)-1]
    # or simply
    lastID = lineList[-1]
    print lastID
    return lastID

#this is the main process
def newProcess():
    #reference the last id in since_ids
    last_id = retrieveLastID() 

    #twitter mentions API endpoint
    twitter_endpoint = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json?screen_name=ApexLegendsBot&since_id='+last_id
    twitter_response, twitter_data = client.request(twitter_endpoint)

    #try to access API to get mentions
    try: 
        tweets = json.loads(twitter_data)    
        print tweets

    except Exception as e: 
        print ''
        print 'Something went wrong when hitting the Twitter API'
        print e
        print ''
        return False

    #use API info
    for ID in tweets:
        screen_name = ID['user']['screen_name']
        str_ID = ID['id']
        text = ID['text']

        print 'This tweeters Username: ' + screen_name
        print ' '
        print 'Tweet: ' + text
        print 'string ID: ' + str(str_ID)

    for idx, tweet in enumerate(tweets):
        time.sleep(1)

        #update batchLastId and append to text file for every tweet    
        since_id = str(tweets[0]['id_str'])       

        #declare date and time for all possible tweets to use
        x = datetime.datetime.now()
        dateDay = x.strftime("%x")
        dateTime = x.strftime("%X")

        text = tweet['text']
        screen_name = tweet['user']['screen_name']

        #for loop through mentions and lookup API
        #1. look up info...if nothing retrieved do nothing
        # If successful, form tweet based on what was retrieved
        # Use an ID so that not every tweet is the "same"
        print ''
        print '-----------Get APEX Stats-----------'

        #split by spaces
        incomingTweet = text.split(' ')
        print(incomingTweet)

        #split further by colon
        newSplit = incomingTweet[1].split(":")
        print 'new'
        print newSplit

        #apply platfrom and username
        if len(incomingTweet) >2 and len(newSplit) >= 2:
            platform = str(newSplit[0]).lower()
            print incomingTweet
            username = newSplit[1] + '%20'+  incomingTweet[2]

        elif len(incomingTweet) >=2 and len(newSplit) >= 2:
            platform = str(newSplit[0]).lower()
            username = newSplit[1]
        
        else:
            platform = 'xbl'
            username = 'Invalid Username'
            
        print (platform)
        print (username)
        
        #loop through each mention and reply
        print 'This is the info to be passed to the API: '
        print 'Platform: ' + platform
        print 'Username: ' + username
        print 'Length of incoming tweet: ' + str(len(incomingTweet))
        print ''

        enter = False

        #transform to True if a valid platofrm is passed
        if str(newSplit[0]).lower() == 'xbl':
            enter = True
        if str(newSplit[0]).lower() == 'psn':
            enter = True
        if str(newSplit[0]).lower() == 'origin':
            enter = True

        print 'Enter Apex API hit session? ' + str(enter)

        #if the info provided can be used...try and hit the Apex API.
        if len(newSplit) >= 2 and enter:

            #try and hit the Apex API
            try:
                r = requests.get('https://public-api.tracker.gg/v2/apex/standard/profile/' + platform + '/' + username,headers=headers)
                print r
                stats = r.json()
                stats_array = {}
                statusCode = r.status_code   
                #print stats
            
            except Exception as e:
                print 'Something went wrong when hitting the Apex API.'
                print e
                return False

            #ensure the API was hit
            print 'Status code: '+str(statusCode)
            print ''

            if statusCode == 200:
                #populate stats dicitionary
                for info in stats['data']['segments'][0]['stats']:
                    index = list(stats['data']['segments'][0]['stats']).index(info)

                    #create key value pairs for the info we want to tweet.
                    key = str(info).upper()
                    value = stats['data']['segments'][0]['stats'][info]['displayValue']

                    #append key value pair to dictionary.
                    stats_array.update({key:value})
                    
                #This string will be tweeted out and will hold the Apex info.
                string = ''
                print 'Stats Info Array:'
                print(stats_array)

                for count, (key, value) in enumerate(stats_array.iteritems(), 0):
                    string += key+': '+value+'\n'
                    if count > 6:
                        break

                #post tweet            
                print ''
                print '-----------Construct Tweet-----------' 
                print ''
                postTweet = 'Hey @'+ screen_name +", here are some stats for '"+username + "'"   +'\n'+'Active Legend: '+str(stats['data']['metadata']['activeLegendName'])+'\n'+string+'\n'+dateDay+' '+dateTime
                print postTweet
                print '-----------Posting Tweet-----------'
                api.update_status(postTweet)
                print '-----------Tweet Posted-----------'
                since_id = str(tweets[idx]['id_str'])

            #nothing was found for info provided
            elif statusCode == 400:
                print 'There is some bad info provided. No Tweet sen out.'

            #server error
            elif statusCode == 500:
                print 'Something is wrong on the APIs end'
            else: 
                print 'The APEX API could not be accessed for some reason.'
        else: 
            print 'No status code logic triggered'      
    if len(tweets) == 0:
        print 'Nothing new on initial start'
        since_id = last_id
    else:
        print 'This is the last_id before the while loop: ' + last_id 
        updateSinceIDs(str(tweets[0]['id_str']))

    return True


