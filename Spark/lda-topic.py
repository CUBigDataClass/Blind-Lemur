from pyspark import SparkConf, SparkContext
from string import printable
from nltk.tokenize import RegexpTokenizer
from langid import classify
from stop_words import get_stop_words

conf = SparkConf().setMaster("local").setAppName("LDA-topic")
sc = SparkContext(conf = conf)


#isEnglish()) takes tweet_text(string) and then returns True if the string is English.
def  isEnglish(tweet_text):
    return classify(tweet_text)[0]=='en'
def  unicode_to_str(u_str):
    return u_str.encode('utf-8')
def toprintable(text):
    return  ''.join(filter(lambda x:x in printable, text))

def tokenize(text):
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(text.lower())
def isStopWord(token):
    en_stop = set(get_stop_words('en'))
    return token not in en_stop

#This should be replaced by querying cassandra
tweets = sc.textFile("tweetsDB.txt")

#cleaning dataset
# 1) filter non-English tweets
engTweets = tweets.filter(isEnglish).map(unicode_to_str)
# 2) remove non-utf8 from the output of the above function
cleanTweets=engTweets.map(toprintable)

#3) Tokenization
tokensRDD= cleanTweets.map(tokenize)
#4) Remove stop_words
tweets=tokensRDD.map(lambda TokenizedTweet:(filter(isStopWord,TokenizedTweet)))
print(tweets.collect())
#5) Remove digits & len(token)<2
#6) Steaming
