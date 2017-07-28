import logging
import os
from pymongo import MongoClient, ASCENDING, DESCENDING

log = None
db = None

def initialize():
    global log
    log = logging.getLogger()
    log.setLevel('DEBUG')
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    log.addHandler(handler)


    global db
    try:
        url = 'mongodb://localhost:27017'
        if 'MONGO_URL' in os.environ:
            url = os.environ['MONGO_URL']

        client = MongoClient(url)
        log.info('Mongo Version: ' + str(client.server_info()['version']))
    except:
        log.error('Can not connect to the DB')
        raise SystemExit

    db = client.patentsview

initialize()
# db = MongoClient('localhost', 27017).patentsview
