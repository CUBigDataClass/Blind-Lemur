url= 'https://gnip-api.twitter.com/search/fullarchive/accounts/{ACCOUNT_NAME}/{LABEL}.json'
username = 'ENTER_USERNAME_HERE'
password = 'ENTER_PASSWORD_HERE'

cassandra_keyspace = 'TwitterStorage'
cassandra_table = 'tweettable'

cassandra_createTableQuery = 'CREATE TABLE twitterstorage.tweettable (tweetid double PRIMARY KEY,hashtags list<text>,retweetcount int,tweet text, tweetdate date)'

