#!/usr/bin/env python
from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
import json
import yaml



import os
import sys

with open("ApiAccessConfig.yaml", 'r') as apiconfig:
    config = yaml.load(apiconfig)
    consumer_key = config["consumer_key"]
    consumer_secret =  config["consumer_secret"]
    access_token_secret =  config["access_token_secret"]
    access_token = config["access_token"]

#Importing SPark
#os.environ['SPARK_HOME'] = "SparkPAth"
#sys.path.append("Py4j PAth")

from pyspark import SparkConf, SparkContext
conf = SparkConf().setMaster("local").setAppName("search-hashtags")
sc = SparkContext(conf = conf)


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    data = api.trends_place(23424977)# 1=woeid =>  Worldwide
    trends =data[0]['trends']
    hashtags = [trend['name'] for trend in trends]
    ListOftrends = '\n'.join(hashtags)
    print(ListOftrends)
    print(len(ListOftrends))

    # stream = Stream(auth, l)
    # stream.filter(???,async=True)
