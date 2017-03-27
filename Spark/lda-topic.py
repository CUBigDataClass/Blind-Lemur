import  os
#check if pyspark env vars are set and then reset to required or delete.
del os.environ['PYSPARK_SUBMIT_ARGS']
from pyspark import SparkConf, SparkContext
import collections

conf = SparkConf().setMaster("local").setAppName("LDA-topic")
sc = SparkContext(conf = conf)

lines = sc.textFile("tweetsDB.txt")
