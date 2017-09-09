url= 'https://gnip-api.twitter.com/search/fullarchive/accounts/.../prod.json'
username = ''
password = ''

cassandra_keyspace = 'twitterstorage'
cassandra_table = 'tweettable'
cassandra_IP= '34.208.209.148'
cassandra_createTableQuery = 'CREATE TABLE IF NOT EXISTS twitterstorage.tweettable (tweetid double PRIMARY KEY,hashtags list<text>,retweetcount int,tweet text, tweetdate date)'
cassandra_keyspace = 'TwitterStorage'
cassandra_table = 'tweettable'
cassandra_topic_table = 'tweetMonthTopics'

cassandra_createTableQuery = 'CREATE TABLE twitterstorage.tweettable (tweetid double PRIMARY KEY,hashtags list<text>,retweetcount int,tweet text, tweetdate date)'

cassandra_create_topic_tableQuery = 'CREATE TABLE tweetMonthTopics (topic text PRIMARY KEY, Month text, Year text, topics frozen<list<tuple<text, float>>>);'


