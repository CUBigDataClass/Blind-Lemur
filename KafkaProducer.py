import yaml
from kafka import KafkaProducer

with open("Kafka.yaml", 'r') as kafkaconfig:
    config = yaml.load(kafkaconfig)
producer = KafkaProducer(bootstrap_servers=[config['bootstrap_servers']])
topic = config['kafka_topic']

producer.send(topic, b'testMessage')
