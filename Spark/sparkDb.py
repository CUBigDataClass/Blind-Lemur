import  config
from pyspark import SparkConf, SparkContext
from pyspark.sql.session import SparkSession
class sparkDb():
    def __init__(self):
        pass

    def readFromCassandra(self, sc):
        spark = SparkSession(sc)
        rdd = spark.read.format("org.apache.spark.sql.cassandra").options(table=config.cassandra_table,
                                                                          keyspace=config.cassandra_keyspace).load().rdd
        return rdd

    def writeToCassandra(self):
        # df.write.format("org.apache.spark.sql.cassandra").mode('append').options(table=config.cassandra_table,
        #                                                                   keyspace=config.cassandra_keyspace).save()
        pass