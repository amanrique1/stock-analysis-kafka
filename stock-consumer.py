import os
from kafka import KafkaConsumer
from json import loads
import datetime
import json
from s3fs import S3FileSystem

ip = os.environ['KAFKA_IP']
port = os.environ['KAFKA_PORT']
bucket = os.environ['BUCKET_NAME']

consumer = KafkaConsumer(
    'stock-analysis',
     bootstrap_servers=[ip+':'+port],
    value_deserializer=lambda x: loads(x.decode('utf-8')))


s3 = S3FileSystem()
datetime_object = datetime.datetime.now()
dat = datetime_object.strftime("%d-%m-%Y_%H-%M-%S")

for count, i in enumerate(consumer):
    with s3.open(f"s3://{bucket}/stock_market_{dat}.json", 'w') as file:
        json.dump(i.value, file)