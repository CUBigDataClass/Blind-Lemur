
from urllib.request import Request
import requests
import config
import json
import time
#https://datastax.github.io/python-driver/installation.html
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
import time
from datetime import datetime
from datetime import datetime, timedelta
from email.utils import parsedate_tz

def createCassandraConnection():
    cluster = Cluster()
    session = cluster.connect()
    session.execute('USE '+config.cassandra_keyspace+';')
    session.execute('DROP TABLE IF EXISTS '+config.cassandra_table+'')
    session.execute(config.cassandra_createTableQuery)
    return session

#return RFC822 compliant string date to UTC dae object
def to_datetime(datestring):
    time_tuple = parsedate_tz(datestring.strip())
    dt = datetime(*time_tuple[:6])
    return dt - timedelta(seconds=time_tuple[-1])

def insertIntoCassandra(data, session):
    for tweet in data["results"]:
        tweet_date= to_datetime(tweet["created_at"])
        tweet_id= tweet["id"]
        tweet_text=tweet["text"]
        retweet_count = tweet["retweet_count"]
        results=[tweet_date,tweet_id,tweet_text,retweet_count]
        batch = BatchStatement()
        insert_data = session.prepare('INSERT INTO '+config.cassandra_table+' (tweetID, tweetDate, retweetCount, tweet) VALUES (?, ?, ?, ?)')
        batch.add(insert_data, (tweet_id, tweet_date, retweet_count, tweet_text))
        session.execute(batch)


if __name__ == "__main__":
    fromDate='201601010000'
    toDate='201701010000'
    query='lang=en'
    PAUSE = 20 # seconds between page requests
    maxResults="500"
    queryString = config.url + '?query=' + query+'&fromDate='+fromDate+'&toDate='+toDate
    # +'&maxResults='+maxResults
    next_token=''
    numOftweets=1000
    maxresults=int(maxResults)
    count=numOftweets/maxresults
    i=0
    session = createCassandraConnection();
    while (next_token is not None) and i<count:
        req = requests.get(queryString, auth=(config.username, config.password))
        results=req.text
        json_out = json.loads(results)
        insertIntoCassandra(json_out, session)
        next_token = json_out['next']
        queryString = config.url + '?query=' + query+'&fromDate='+fromDate+'&toDate='+toDate+'&next='+next_token
        # +'&maxResults='maxResults
        time.sleep(PAUSE)
        # print(req.text)
        i+=1