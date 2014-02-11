# Creates follower.json, which maps follower -> unique_integer
# Creates Connections.json, which maps user --. [follower0, follower1.....]
#

import json
import os.path
import tweepy
import time
from collections import defaultdict


substance = 'test'
with open('%s_tweeters.json' %substance,'rb') as js:
    tweeters = json.load(js)
    
with open('tokens.json','rb') as js:
    tokens = json.load(js)
    consumer_key = tokens["consumer_key"]
    consumer_secret = tokens["consumer_secret"]
    access_token = tokens["access_token"]
    access_token_secret = tokens["access_token_secret"]


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


if os.path.isfile('%s_followers.json' %substance):
    with open('%s_followers.json' %substance,'rb') as js:
        followers = json.load(js)
else:
    followers = defaultdict(list)        
    

for u_id in tweeters:
    for page in tweepy.Cursor(api.followers_ids, user_id = u_id).pages():
        if page not in followers[u_id] :
            followers[u_id].append(page)
            time.sleep(5) #waiting for twitter
            
            
with open('%s_followers.json' %substance, 'wb') as js:
    json.dump(followers, js)
print(followers)



         