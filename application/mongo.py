import logging
from application.utils import globals
from application.utils.helpers import Singleton
from pymongo import MongoClient, ASCENDING, DESCENDING


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
            logging.error('DB error: %s' % error.message)
            raise error

    def generate_structure(self):
        """
        Create indexes
        :return:
        """
        try:
            self.db.twitter.ensure_index([('created', DESCENDING)], name='_date_index1', background=True)
            self.db.twitter.ensure_index([('source', ASCENDING)], name='_source_index1', background=True)
            self.db.twitter.ensure_index([('hashtags', ASCENDING)], name='_hashtags_index1', background=True)
            self.db.twitter.ensure_index([('user', ASCENDING)], name='_user_index1', background=True)
        except Exception, error:
            logging.error('Error during index creation: %s' % error.message)
            raise error
