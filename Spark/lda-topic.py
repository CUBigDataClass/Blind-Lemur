from pyspark import SparkConf, SparkContext
from string import printable
from nltk.tokenize import RegexpTokenizer
from langid import classify
from stop_words import get_stop_words
from string import digits
from nltk.stem.porter import PorterStemmer
from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.mllib.linalg import Vectors

conf = SparkConf().setMaster("local").setAppName("LDA-topic")
sc = SparkContext(conf = conf)
tokenizer = RegexpTokenizer(r'\w+')
# create English stop words set
en_stop = set(get_stop_words('en'))

#isEnglish()) takes tweet_text(string) and then returns True if the string is English.
def  isEnglish(tweet_text):
    return classify(tweet_text)[0]=='en'
def  unicode_to_str(u_str):
    return u_str.encode('utf-8')
def toprintable(text):
    return  ''.join(filter(lambda x:x in printable, text))

def tokenize(text):
    return tokenizer.tokenize(text.lower())
def isStopWord(token):
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
stopped_tokens=tokensRDD.map(lambda TokenizedTweet:(filter(isStopWord,TokenizedTweet)))

#5) Remove digits & len(token)<2
tweets_alpha=stopped_tokens.map(lambda tweet:(filter(str.isalpha,tweet)))
tweets_tokens=tweets_alpha.map(lambda tweet:filter(lambda x: len(x) >2 , tweet))
# Remove empty list of tokens
cleanText=tweets_tokens.filter(lambda tokens: tokens)
# print(cleanText.collect())
#6) Steaming
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
# replace map by flatmap if you want to flatten the list
stemmed_tokens = cleanText.map(lambda token: map(p_stemmer.stem,token))
# Remove unicode & convert each token to string
str_tokens= stemmed_tokens.map(lambda tokens : map(str,tokens))
# print(stemmed_tokens.map(lambda tokens : map(str,tokens)).collect())
