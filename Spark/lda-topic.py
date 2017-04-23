from pyspark import SparkConf, SparkContext
from string import printable
from nltk.tokenize import RegexpTokenizer
from langid import classify
from stop_words import get_stop_words
from string import digits
from nltk.stem.porter import PorterStemmer
from pyspark.mllib.clustering import LDA, LDAModel
from pyspark.mllib.linalg import Vectors
from collections import defaultdict
import sparkDb
import config

conf = SparkConf().setAppName("LDA-topic").set("spark.cassandra.connection.host", config.cassandra_IP).set("spark.cassandra.connection.port", "9042")
sc = SparkContext(conf = conf)
tokenizer = RegexpTokenizer(r'\w+')
path = '/root/output'
en_stop = set(get_stop_words('en')) # create English stop words set
num_topics = 100            # Number of topics we are looking for
num_words_per_topic = 10    # Number of words to display for each topic
max_iterations = 35         # Max number of times to iterate before finishing
token_frequency = defaultdict(int) # Dictionary - word: frequency
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

sparkdb = sparkDb.sparkDb()
rdd = sparkdb.readFromCassandra(sc)
tweets = rdd.map(lambda row: row[3]).map(toprintable).map(str)


#cleaning dataset
# 1) filter non-English tweets
engTweets = tweets.filter(isEnglish).map(str).sample(False,0.2).take(1000)
# 2) remove non-utf8 from the output of the above function
cleanTweets=sc.parallelize(engTweets).map(toprintable)

#added function to retrieve rdd from cassandra
# sparkdb = sparkDb()
# rdd = sparkdb.readFromCassandra(sc)

#3) Tokenization
tokensRDD= cleanTweets.map(tokenize)
#4) Remove stop_words
stopped_tokens=tokensRDD.map(lambda TokenizedTweet:[token for token in TokenizedTweet  if token not in en_stop])

#5) Remove digits & len(token)<2
tweets_alpha=stopped_tokens.map(lambda TokenizedTweet:[token for token in TokenizedTweet  if token.isalpha()])
tweets_tokens=tweets_alpha.map(lambda TokenizedTweet:[token for token in TokenizedTweet  if len(token)>2])
# Remove empty list of tokens
cleanText=tweets_tokens.filter(lambda tokens: tokens)

#6) Steaming
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
# replace map by flatmap if you want to flatten the list
stemmed_tokens = cleanText.map(lambda TokenizedTweet:[p_stemmer.stem(token) for token in TokenizedTweet])
# Remove unicode & convert each token to string
flat_tokens= stemmed_tokens.flatMap(lambda tokens :[x for x in tokens])

frq_words = flat_tokens.map(lambda word: (word,1)).reduceByKey(lambda a, b: a + b).map(lambda tuple: (tuple[1], tuple[0])).sortByKey(False)

filteredList= frq_words.filter(lambda pair: pair[0]>1).map(lambda x: x[1]).zipWithIndex().collectAsMap()

# # Convert the given document into a vector of word counts
def document_vector(document):
    id = document[1]
    counts = defaultdict(int)
    for token in document[0]:
        if token in filteredList:
            token_id = filteredList[token]
            counts[token_id] += 1
    counts = sorted(counts.items())
    keys = [x[0] for x in counts]
    values = [x[1] for x in counts]
    return (id, Vectors.sparse(len(filteredList), keys, values))
# Now the dataset is clean

corpus = stemmed_tokens.zipWithIndex().map(document_vector).map(list)
print(corpus.count())
# Cluster the documents into three topics using LDA
lda_model = LDA.train(corpus, k=num_topics, maxIterations=max_iterations)
topic_indices = lda_model.describeTopics(maxTermsPerTopic=num_words_per_topic)
inv_voc = {value: key for (key, value) in filteredList.items()}
results=[]

    # Print topics, showing the top-weighted 10 terms for each topic
for i in range(len(topic_indices)):
    for j in range(len(topic_indices[i][0])):
        results.append((str(inv_voc[topic_indices[i][0][j]]), topic_indices[i][1][j]))

result = sc.parallelize(results).collect()

print(result)
