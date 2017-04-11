import  config
class sparkDb():
    def __init__(self):
        pass

    def readFromCassandra(self):
        from pyspark import SparkConf, SparkContext
        from pyspark.sql.session import SparkSession
        conf = SparkConf().setMaster("local").setAppName("testCassandra")

        sc = SparkContext(conf=conf)

        spark = SparkSession(sc)

        rdd = spark.read.format("org.apache.spark.sql.cassandra").options(table=config.cassandra_table,
                                                                          keyspace=config.cassandra_keyspace).load().rdd

        return rdd

    def writeToCassandra(self):
        pass