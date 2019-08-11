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

#twitter validation
auth = tweepy.OAuthHandler(cfg.consumer_key, cfg.consumer_secret)
auth.set_access_token(cfg.access_token, cfg.access_token_secret)

api = tweepy.API(auth)

#apex validationddd
headers = {
        'TRN-Api-Key': '3c0a15fd-ac7c-4f37-9f7a-47bd7a76286d',
    }

#setup retrieve mentions
consumer = oauth.Consumer(key=cfg.consumer_key, secret=cfg.consumer_secret)
access_token = oauth.Token(key=cfg.access_token, secret=cfg.access_token_secret)
client = oauth.Client(consumer, access_token)

#define the initial entrance point 
since_id = '1160594273093529600'

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

def process():
    

    print '-----------Initial Start-----------'
    print ' '
        
    #twitter API    
    twitter_endpoint = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json?screen_name=ApexLegendsBot&since_id=' + '1159970903654043648'

    twitter_response, twitter_data = client.request(twitter_endpoint)

    #access API to get mentions
    tweets = json.loads(twitter_data)    

    #use API info
    for ID in tweets:
        screen_name = ID['user']['screen_name']
        str_ID = ID['id']
        text = ID['text']

        print 'This tweeters Username: ' + screen_name
        print ' '
        print 'Tweet: ' + text
        print 'string ID: ' + str(str_ID)

    #array to hold mentions info
    info = {}

    for tweet in tweets:
        time.sleep(1)

        #declare date and time for all possible tweets to use
        x = datetime.datetime.now()
        dateDay = x.strftime("%x")
        dateTime = x.strftime("%X")

        text = tweet['text']
        screen_name = tweet['user']['screen_name']

        #append to dictionary
        #info.update({text:screen_name})

        #for loop through mentions and lookup API
        #1. look up info...if nothing retrieved do nothing
        # If successful, form tweet based on what was retrieved
        # Use an ID so that not every tweet is the "same"
        print ''
        print '-----------Get APEX Stats-----------'
        
        #loop through each mention and reply
        #print tweets
        incomingTweet = text.split(' ')
        transformTweet = str(incomingTweet[1])
        splitTweet = transformTweet.split(':')

        #handle undesrcore
        additionalText = text.split(':')
        underscoreRight = additionalText[1].split('_')
        print 'This is the info to be passed to the API: '+str(splitTweet)
        print ''

        #determing whether the platform is one of the three options
        #this seems to break the API entirely if this is not correct
        #username can remain incorrect

        enter = False

        #transform to True if a valid platofrm is passed
        if str(splitTweet[0]) == 'xbl':
            enter = True
        if str(splitTweet[0]) == 'psn':
            enter = True
        if str(splitTweet[0]) == 'origin':
            enter = True
                
        #asign the platform and username
        if len(splitTweet) == 2 and enter:

            #assign platform
            platform = str(splitTweet[0])
            username = str(splitTweet[0])

            headers = {
                'TRN-Api-Key': cfg.APEX_KEY
            }

            print 'Username: ' + username
            print ''

            
            #try and hit API
            
            r = requests.get('https://public-api.tracker.gg/v1/apex/standard/profile/' + platform + '/' + username,headers=headers)
            stats = r.json()
            stats_array = {}
            statusCode = r.status_code   

            #ensure the API was hit
            print 'Status code: '+str(statusCode)
            print ''

            if statusCode == 200:

                #populate stats dicitionary
                for info in stats['data']['stats']:
                    index = stats['data']['stats'].index(info)
                    key = str(stats['data']['stats'][index]['metadata']['key']).upper()
                    value = str(stats['data']['stats'][index]['value'])
                    stats_array.update({key:value})

                string = ''

                print(stats_array)
                #for key, value in stats_array.iteritems():
                for count, (key, value) in enumerate(stats_array.iteritems(), 0):
                    # print 'Iteration: ' + str(count)
                    # print key,value
                    #print key, value
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
                #print postTweet
                #api.update_status(postTweet)
                print '-----------Tweet Posted-----------'
                
            
                #set new max id to the first entry to come in
                since_id = str(tweets[0]['id_str'])
                print 'This is the since_id for this tweet: ' + since_id
                 

            #nothing returned from API
            elif statusCode == 400:
                #platform = splitTweet[1]
                print 'There is some bad info provided'
                print ''
                postTweet = 'Hey @'+ screen_name + ", nothing found for '" + username + "' on '" +platform+ "'"+'.' '\n'+dateDay+' '+dateTime
                print postTweet
                
                
                
            else: 
                print 'The APEX API could not be accessed for some reason.'
        else: 
            print 'Bad info.'
            # postTweet = 'Hey @'+ screen_name + ', the information you provided was blasphemous. Please follow the guidelines when using this bot. I was created by a human!'+'\n'+dateDay+' '+dateTime
            # print postTweet
            
    else:
        print 'nothing new on initial start'


    #time.sleep(60)

    #enter While loop section
    ############################################################################################################################################################################################################
    ############################################################################################################################################################################################################
    ############################################################################################################################################################################################################
    ############################################################################################################################################################################################################
    ############################################################################################################################################################################################################

    while 1>0:
        time.sleep(1)

        #declare date and time for all possible tweets to use
        x = datetime.datetime.now()
        dateDay = x.strftime("%x")
        dateTime = x.strftime("%X")

        print '-----------While Loop Iteration Start-----------'
        print ' '        
            
        twitter_endpoint = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json?screen_name=ApexLegendsBot' + '&since_id=' + since_id

        twitter_response, twitter_data = client.request(twitter_endpoint)

        #access API to get mentions
        tweets = json.loads(twitter_data)    

        #detemine if there are new tweets
        if len(tweets) != 0:
            print tweets

            #use API info
            for ID in tweets:
                screen_name = ID['user']['screen_name']
                str_ID = ID['id']
                text = ID['text']

                print 'This bots Username: ' + screen_name
                print ' '
                print 'Tweet: ' + text
                print 'string ID: ' + str(str_ID)

            for tweet in tweets:

                text = tweet['text']
                screen_name = tweet['user']['screen_name']

                #for loop through mentions and lookup API
                #1. look up info...if nothing retrieved do nothing
                # If successful, form tweet based on what was retrieved
                # Use an ID so that not every tweet is the "same"
                print ''
                print '-----------Get APEX Stats-----------'
                
                print '-----------Get APEX Stats-----------'
        
        #loop through each mention and reply
        #print tweets
                incomingTweet = text.split(' ')
                transformTweet = str(incomingTweet[1])
                splitTweet = transformTweet.split(':')

                #handle undesrcore
                additionalText = text.split(':')
                underscoreRight = additionalText[1].split('_')
                print 'This is the info to be passed to the API: '+str(splitTweet)
                print ''

                #determing whether the platform is one of the three options
                #this seems to break the API entirely if this is not correct
                #username can remain incorrect

                enter = False

                #transform to True if a valid platofrm is passed
                if str(splitTweet[0]) == 'xbl':
                    enter = True
                if str(splitTweet[0]) == 'psn':
                    enter = True
                if str(splitTweet[0]) == 'origin':
                    enter = True
                        
                #asign the platform and username
                if len(splitTweet) == 2 and enter:

                    #assign platform
                    platform = str(splitTweet[0])
                    username = str(splitTweet[1])

                    print 'Username: ' + username
                    print ''

                    
                    #try and hit API
                    
                    r = requests.get('https://public-api.tracker.gg/v1/apex/standard/profile/' + platform + '/' + username,headers=headers)
                    stats = r.json()
                    stats_array = {}
                    statusCode = r.status_code   

                    #ensure the API was hit
                    print 'Status code: '+str(statusCode)
                    print ''

                    if statusCode == 200:

                        #populate stats dicitionary
                        for info in stats['data']['stats']:
                            index = stats['data']['stats'].index(info)
                            key = str(stats['data']['stats'][index]['metadata']['key']).upper()
                            value = str(stats['data']['stats'][index]['value'])
                            stats_array.update({key:value})

                        string = ''

                        print(stats_array)
                        #for key, value in stats_array.iteritems():
                        for count, (key, value) in enumerate(stats_array.iteritems(), 0):
                            # print 'Iteration: ' + str(count)
                            # print key,value
                            #print key, value
                            string += key+': '+value+'\n'
                            if count > 6:
                                break

                        #construct tweet            
                        print ''
                        print '-----------Construct Tweet-----------' 
                        print ''
                        postTweet = 'Hey @'+ screen_name +", here are some stats for '"+username + "'"   +'\n'+'Active Legend: '+str(stats['data']['metadata']['activeLegendName'])+'\n'+string+'\n'+dateDay+' '+dateTime
                        
                        #post tweet
                        print postTweet
                        print '-----------Posting Tweet-----------' 
                        api.update_status(postTweet)
                        print '-----------Tweet Posted-----------' 
                        
                    
                        #set new max id to the first entry to come in
                        since_id = str(tweets[0]['id_str'])
                        print 'This is the since_id for this tweet: ' + since_id 

                    #nothing returned from API
                    elif statusCode == 400:
                        #platform = splitTweet[1]
                        print 'There is some bad info provided'
                        print ''
                        postTweet = 'Hey @'+ screen_name + ", nothing found for '" + username + "' on '" +platform+ "'"+'.' '\n'+dateDay+' '+dateTime
                        print postTweet
                        print '-----------Posting Tweet-----------' 
                        api.update_status(postTweet)
                        print '-----------Tweet Posted-----------' 
                        since_id = str(tweets[0]['id_str'])
                        time.sleep(1)
                        
                        
                    else: 
                        print 'The APEX API could not be accessed for some reason.'
                        since_id = str(tweets[0]['id_str'])
                        time.sleep(1)
                else: 
                    print 'Bad info.'
                    #postTweet = 'Hey @'+ screen_name + ', the information you provided was blasphemous. Please follow the guidelines when using this bot. I was created by a human!'+'\n'+dateDay+' '+dateTime
                    #print postTweet

                time.sleep(1)

                    

        elif len(tweets) == 0:
            
            print 'There is nothing new. The bot will re-loop in 60 seconds'



            time.sleep(60)

            
process()