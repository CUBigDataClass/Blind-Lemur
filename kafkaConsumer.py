from kafka import KafkaConsumer
import yaml

with open("Kafka.yaml", 'r') as kafkaconfig:
    config = yaml.load(kafkaconfig)
consumer = KafkaConsumer(bootstrap_servers= config['bootstrap_servers'],
                         auto_offset_reset='earliest')
consumer.subscribe([config['kafka_topic']])

for message in consumer:
    print (message)
