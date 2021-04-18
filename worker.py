import os
import redis
from rq import Worker, Queue, Connection, SimpleWorker
import object_detection
from object_detection import import_model

# print('Importing object detection model')
# object_detection.import_model()

listen = ['default']

conn = redis.from_url('redis://localhost:6379')

if __name__ == '__main__':
    with Connection(conn):
        import_model()
        worker = SimpleWorker(list(map(Queue, listen)))
        worker.work()
