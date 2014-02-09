# Uses followers.json to create dictionary disciples
# disciples is similar to users from getTweeters.py
# it maps followers from follower.json -> unique_integer

import json
import os.path
import networkx as nx

substance = 'test'
with open('%s_followers.json' %substance,'rb') as js:
    followers = json.load(js)
with open('%s_tweeters.json' %substance,'rb') as js:
    users = json.load(js)

if os.path.isfile('%s_disciples.json' %substance):
    with open('%s_disciples.json' %substance,'rb') as js:
        disciples = json.load(js)
        counter = disciples['max']
else:
    disciples = dict()
    disciples['max'] = 0
    counter = 0
    
for u_id in followers:
    for follower in followers[u_id]:
        for user in follower:
            if user not in disciples:
                disciples[user] = counter
                counter+=1
 
disciples['max'] = counter  
with open('%s_disciples.json' %substance, 'wb') as js:
    json.dump(disciples, js)
    
DG = nx.DiGraph()
DG.add
