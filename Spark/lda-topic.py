from pyspark import SparkConf, SparkContext
from textblob import TextBlob

conf = SparkConf().setMaster("local").setAppName("LDA-topic")
sc = SparkContext(conf = conf)

def  isEnglish(tweet_text):
    if(len(tweet_text)>2):
        b=TextBlob(u""+tweet_text)
        b.detect_language() =='en'

#This should be replace by querying cassandra
tweets = sc.textFile("tweetsDB.txt")

#cleaning dataset
# 1) filter non-English tweets
rdd = tweets.filter(isEnglish).collect()
