#import all the necessary libraries

import tweepy
import re
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import pandas as pd
import matplotlib.pyplot as plt

#register the keys and tokens
consumer_key = 'Uuvdom7hjb75PDIwikZaYj9DF'
consumer_secret = 'wEUYgWBUSaRNW1yyuGcSN9UNAOwt0WUAaYePX6eOgHMs5RJglx'
access_token = '917510546785800192-eN5Jqn1w78xy1ysHHsjQOQrPdGDI2QI'
access_secret = 'gsYqFqIiPMEPYWNLnXuWjmmuJTNw6vIE8PVX5lrkgJExT'

#authenticate tokens
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

# define MyListener
class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open('data.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

#Search twitter stream for the tags specified
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#ISIS','#IS','#ISIL','#Islamic_State'])

#Create a dataframe with the tweets by opening the json file
tweets_data=list()
f=open('data.json','r')
lines=f.readlines()

for i in range(0,len(lines)):
    if lines[i].startswith('{'):
        tweet=json.loads(lines[i])
        tweets_data.append(tweet)

tweets=pd.DataFrame(tweets_data)

#Manipulate data to obtain countries distribution
countries={}
none_count=0
for i in range(0,len(tweets)):
    if (tweets.ix[i,'place']==None):
        none_count=none_count+1
    elif tweets.ix[i,'place']['country'] in countries:
        countries[(tweets.ix[i,'place']['country'])] = countries[(tweets.ix[i,'place']['country'])]+1
    else:
        countries[(tweets.ix[i,'place']['country'])] = 1

##none count = 20280 so no point in plotting countries


#Plot tweets by language
tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
xaxis=[-0.1,0.9,1.9,2.9,3.9]
patches, labels = ax.get_legend_handles_labels()
ax.legend(patches, labels, loc='best')
for i in range(len(tweets_by_lang[:5])):
    ax.text(xaxis[i], tweets_by_lang[i],str(tweets_by_lang[i]))
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

#Define function to process text
def word_in_text(word, text):
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    return False

#Get tweets by tag
tweets['ISIS'] = tweets['text'].apply(lambda tweet: word_in_text('ISIS', tweet))
tweets['ISIL'] = tweets['text'].apply(lambda tweet: word_in_text('ISIL', tweet))
tweets['IS'] = tweets['text'].apply(lambda tweet: word_in_text('IS', tweet))
tweets['Islamic_State'] = tweets['text'].apply(lambda tweet: word_in_text('Islamic_State', tweet))


print(tweets['ISIS'].value_counts()[True])
print(tweets['ISIL'].value_counts()[True])
print(tweets['IS'].value_counts()[True])
print(tweets['Islamic_State'].value_counts()[True])

tweet_tags = ['ISIS', 'ISIL', 'IS','Islamic_State']
tweets_by_tag = [tweets['ISIS'].value_counts()[True], tweets['ISIL'].value_counts()[True], tweets['IS'].value_counts()[True],tweets['Islamic_State'].value_counts()[True]]

#Plot tweets by tag
x_pos = list(range(len(tweet_tags)))
width = 0.8
fig, ax = plt.subplots()
xaxis=[-0.1,1,1.9,3]
for i in range(len(tweets_by_tag)):
    ax.text(xaxis[i], tweets_by_tag[i],str(tweets_by_tag[i]))

plt.bar(x_pos, tweets_by_tag, width, alpha=1, color='g')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_xlabel('Tags', fontsize=10)
ax.set_title('Tags Distribution', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.05 * width for p in x_pos])
ax.set_xticklabels(tweet_tags)





