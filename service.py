import config
import CassandraManager


if __name__ == "__main__":
    month = 'Dec'
    rows = CassandraManager.readTopicsFromCassandra(month)
    for row in rows:
        print(row.topic, row.topics )