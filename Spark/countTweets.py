from pyspark import SparkConf, SparkContext
from string import printable
from ast import literal_eval
import sparkDb
import config

conf = SparkConf().setMaster("local").setAppName("LDA-topic")
sc = SparkContext(conf = conf)

def toprintable(text):
    return  ''.join(filter(lambda x:x in printable, text))
def has_topic(tweet,topic):
    return topic in tweet
def parseLine(line):
    (word, weight)=literal_eval(line)
    return (word, weight)
LDA_topics= sc.textFile("/Users/amjad/git/Blind-Lemur/DEC_TOPICS/part-00[0-3]*").map(parseLine).filter(lambda LDA_tuple: LDA_tuple[1]>0.007).collect()

sparkdb = sparkDb.sparkDb()
rdd = sparkdb.readFromCassandra(sc)
tweetsRDD = rdd.map(lambda row: row[3]).map(toprintable).map(str)

tweets = rdd.map(lambda row: row[3]).map(toprintable).map(str)
#num_tweets is a list in this format [(topic1,weight,tweet_count),(topic2,weight,tweet_count) ]
num_tweets= [(LDA_tuple[0],LDA_tuple[1],tweets.filter(lambda tweet: has_topic(tweet,LDA_tuple[0])).count()) for LDA_tuple in LDA_topics]
