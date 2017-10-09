import tweepy
# only used to get the sensitive login info from a pickle
import pickle

# load the access tokens
with open('../pickles/twitter_access.p', 'r') as f:
    cfg = pickle.load(f)
# cfg is of the form:
# cfg = {'access_token': 'xxxx',
#       'access_token_secret': 'xxxx',
#       'consumer_key': 'xxxx',
#       'consumer_secret': 'xxxx'}


# create the authentication handler object
auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
# link it to the specific application
auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])

# 'build' the api
t_api = tweepy.API(auth)
# now you can start to interact with twitter...

timeline = t_api.user_timeline()
last_tweet = timeline[0]
print last_tweet.text

# tweet
a_tweet = u"my super awesome tweet"
t_api.update_status(status=a_tweet)

# destroy the last tweet
timeline = t_api.user_timeline()
last_tweet = timeline[0]
t_api.destroy_status(last_tweet.id)
