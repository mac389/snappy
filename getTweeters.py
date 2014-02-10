# Creates json file to store dictionary mapping users ---> unique_integer
#
#

import json
import os.path

substance = 'test'
f = open('%s_all_out.txt' %substance)
if os.path.isfile('%s_tweeters.txt' %substance):
    with open('%s_tweeters.json' %substance,'rb') as js:
        users = json.load(js)
        counter = users['max']
else:
    users = dict()
    users['max']=0
    counter = 0
    
for line in f:
    start_position = line.find('user : {"id"=>')+14
    end_position = line.find(', "id_str"=>')
    user_id = line[start_position:end_position]
    if user_id not in users:
        users[user_id] = counter
        counter+=1
    #else:
    #    print("already there\n")
f.close()
users['max']=counter

with open('%s_tweeters.json' %substance, 'wb') as js:
    json.dump(users, js)
print(users)

