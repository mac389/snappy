import twitter, json

READ = 'rb'
tokens = json.load(open('../tokens.json',READ))

api = twitter.Api(**tokens['twitter'])

#to find a social network, we must look by people, not topics
#what about looking by region