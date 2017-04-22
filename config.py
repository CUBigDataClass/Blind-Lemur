url= 'https://gnip-api.twitter.com/search/fullarchive/accounts/greg-students/prod.json'
username = 'abu.sayed@colorado.edu'
password = ''


cassandra_keyspace = 'twitterstorage'
cassandra_table = 'tweettable'
cassandra_IP= '34.208.209.148'
cassandra_createTableQuery = 'CREATE TABLE IF NOT EXISTS twitterstorage.tweettable (tweetid double PRIMARY KEY,hashtags list<text>,retweetcount int,tweet text, tweetdate date)'
