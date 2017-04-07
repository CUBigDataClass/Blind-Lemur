from datetime import datetime
from datetime import datetime, timedelta
from email.utils import parsedate_tz
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
import config
import re

def createCassandraConnection():
    cluster = Cluster()
    session = cluster.connect()
    session.execute('USE '+config.cassandra_keyspace+';')
    #session.execute('DROP TABLE IF EXISTS '+config.cassandra_table+'')
    session.execute(config.cassandra_createTableQuery)
    return session

#return RFC822 compliant string date to UTC date object
def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])

def insertIntoCassandra(data, session):
    num_tweets = 0
    for tweet in data["results"]:
        num_tweets += 1
        hashtagList=[]
        tweet_date= to_datetime(tweet["created_at"])
        tweet_id= tweet["id"]
        tweet_text=tweet["text"]
        tweet_text = re.sub(r"(?:\@|https?\://)\S+", "", tweet_text)
        place = tweet["place"]
        hashtags = tweet["entities"]["hashtags"]
        for hashtag in hashtags:
            hashtagList.append(hashtag['text'])
        retweet_count = tweet["retweet_count"]

        batch = BatchStatement()
        insert_data = session.prepare('INSERT INTO '+config.cassandra_table+' (tweetID, tweetDate, retweetCount, tweet, hashtags) VALUES (?, ?, ?, ?, ?)')
        batch.add(insert_data, (tweet_id, tweet_date, retweet_count, tweet_text, hashtagList))
        session.execute(batch)
    print(num_tweets)