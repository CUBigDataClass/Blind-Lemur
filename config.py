url= 'https://gnip-api.twitter.com/search/fullarchive/accounts/greg-students/prod.json'
username = 'abu.sayed@colorado.edu'
password = 'Blind-Lemur'

# Follow Kafka and zookeeper installation steps here: https://kafka.apache.org/quickstart

bootstrap_servers= "localhost:9092"
kafka_topic = "kafkatopic"


cassandra_keyspace= 'TwitterStorage'
cassandra_createTableQuery= 'CREATE TABLE tweetTable (tweetID double PRIMARY KEY, tweetDate date, retweetCount int, tweet text);'
cassandra_table = cassandra_keyspace+'.'+'tweetTable'