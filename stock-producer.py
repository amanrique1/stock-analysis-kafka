import requests
from kafka import KafkaProducer
from json import dumps
import os

ip = os.environ['KAFKA_IP']
port = os.environ['KAFKA_PORT']

producer = KafkaProducer(bootstrap_servers=[ip+':'+port], #change ip here
                        value_serializer=lambda x: dumps(x).encode('utf-8'))

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=BC5NJ8CLG6T5NQZT'
r = requests.get(url)
data = r.json()

#Send the first value to Kafka (most recent record)
producer.send('stock-analysis', value={'ibm':data['Time Series (5min)'][next(iter(data['Time Series (5min)']))]})

#clear data from kafka producer
producer.flush()