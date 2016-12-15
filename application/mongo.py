import logging
from datetime import datetime as dt
from pymongo import MongoClient, ASCENDING, DESCENDING
from utils.helpers import Singleton


@Singleton
class Connection:
    _client = None
    db = None

    def __init__(self):
        pass

    def setup(self, mongo_uri, mongo_db):
        try:
            self._client = MongoClient(mongo_uri)
            self.db = self._client[mongo_db]
            self.generate_structure()
        except Exception, error:
            logging.error("DB error: %s" % error.message)
            raise error

    def generate_structure(self):
        try:
            self.db.twitter.ensure_index([('created', DESCENDING)], name='_date_index1', backround=True)

            self.db.twitter.ensure_index([('source', ASCENDING)], name='_source_index1', backround=True)

            self.db.twitter.ensure_index([('hashtags', ASCENDING)], name='_hashtags_index1', backround=True)
        except Exception, error:
            logging.error("Error during index creation: %s" % error.message)
            raise error

    def insert(self, collection, data):
        if collection == 'twitter':
            data['created'] = dt.now()
            data['source'] = 'listener'
            self.db.twitter.insert_one(data)
        else:
            raise TypeError
