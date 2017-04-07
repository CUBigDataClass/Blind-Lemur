This branch creates interfaces for using cassandra DB, uses cassandra driver.
Reference: https://datastax.github.io/python-driver/installation.html

Steps:
Install Cassandra
Bring Cassandra UP
Create a Keyspace name through cqlsh with the name as given in the config file with th atrribute cassandra_keyspace
Run getTweets to store data into the cassandra



#Some steps-

pip3 install cassandra-driver

If for some reason, you get a permission denied error, you need to give permissions to the user

sudo chown -R USERNAME /home/ckamat/.cache/pip grants permission to the user.


To upgrade pip3

sudo pip3 install --upgrade pip

Cassandra-driver version is 3.8.1



