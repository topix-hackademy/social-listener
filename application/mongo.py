import logging
from datetime import datetime as dt
from pymongo import MongoClient, ASCENDING, DESCENDING
from utils.helpers import Singleton
from application import globals


@Singleton
class Connection:
    _client = None
    db = None

    def __init__(self):
        try:
            self._client = MongoClient(globals.configuration.mongo['uri'])
            self.db = self._client[globals.configuration.mongo['db']]
            self.generate_structure()
        except Exception, error:
            logging.error("DB error: %s" % error.message)
            raise error

    def generate_structure(self):
        """
        Create indexes
        :return:
        """
        try:
            self.db.twitter.ensure_index([('created', DESCENDING)], name='_date_index1', backround=True)

            self.db.twitter.ensure_index([('source', ASCENDING)], name='_source_index1', backround=True)

            self.db.twitter.ensure_index([('hashtags', ASCENDING)], name='_hashtags_index1', backround=True)
        except Exception, error:
            logging.error("Error during index creation: %s" % error.message)
            raise error

    def insert(self, collection, data):
        """
        Insert new data in a specific collection
        :param collection: Collection Name
        :param data: Data to insert
        :return:
        """
        if collection == 'twitter':
            data['created'] = dt.now()
            data['source'] = 'listener'
            self.db.twitter.insert_one(data)
        else:
            raise TypeError
