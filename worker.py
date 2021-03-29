import os
import redis
from rq import Worker, Queue, Connection
import object_detection

# print('Importing object detection model')
# object_detection.import_model()

listen = ['default']

conn = redis.from_url('redis://localhost:6379')

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
