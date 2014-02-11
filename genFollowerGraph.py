# Uses followers.json to create dictionary disciples
# disciples is similar to users from getTweeters.py
# it maps followers from follower.json -> unique_integer
# Creates a directed graph of tweeters --> followers

import json
import os.path
import networkx as nx
from networkx import linalg
import matplotlib.pyplot as plt
    
substance = 'test'
with open('%s_followers.json' %substance,'rb') as js:
    followers = json.load(js)
with open('%s_tweeters.json' %substance,'rb') as js:
    tweeters = json.load(js)

if os.path.isfile('%s_disciples.json' %substance):
    with open('%s_disciples.json' %substance,'rb') as js:
        disciples = json.load(js)
        counter = disciples['max']
else:
    disciples = dict()
    disciples['max'] = 0
    counter = 0
    
for u_id in followers:
    for followerlist in followers[u_id]:
        for user in followerlist:
            if user not in disciples:
                disciples[user] = counter
                counter+=1
 
disciples['max'] = counter  
with open('%s_disciples.json' %substance, 'wb') as js:
    json.dump(disciples, js)
    
DG = nx.DiGraph()

for u_id in followers:
    for followerlist in followers[u_id]:
        for user in followerlist:
            DG.add_edge(tweeters[u_id],disciples[user])
 
laplacian = linalg.laplacianmatrix.directed_laplacian_matrix(DG)
print(laplacian)
nx.write_dot(DG,"linus.dot")