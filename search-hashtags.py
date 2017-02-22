from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import json

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""


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
