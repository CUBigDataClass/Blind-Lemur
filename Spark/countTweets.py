from pyspark import SparkConf, SparkContext
from string import printable
import sparkDb
import config

conf = SparkConf().setMaster("local").setAppName("LDA-topic")
sc = SparkContext(conf = conf)

def toprintable(text):
    return  ''.join(filter(lambda x:x in printable, text))
    
def has_topic(tweet,topic):
    return topic in tweet

sparkdb = sparkDb.sparkDb()
rdd = sparkdb.readFromCassandra(sc)
tweets = rdd.map(lambda row: row[3]).map(toprintable).map(str)
num_topics= tweets.filter(lambda tweet: has_topic(tweet,"app")).count()

print(num_topics)
