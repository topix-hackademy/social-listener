import tweepy
import logging
from application.mongo import Connection
from application.utils.helpers import what_time_is_it


class TwitterStreamingListener(tweepy.StreamListener):

    def __init__(self, keywords):
        super(TwitterStreamingListener, self).__init__()
        self.keywords = keywords

    def on_status(self, tweet):
        """
        If new tweet is received, this function will be called.
        For each tweet will create a new Mongo Insert
        :param tweet:
        :return:
        """
        try:
            Connection.Instance().db.twitter.insert_one(
                {
                    'source': 'listener',
                    'data': tweet._json,
                    'keywords': self.keywords,
                    'created': what_time_is_it()
                })
        except Exception as e:
            logging.error("MongoDB Insert Error in listener: " + e)

    def on_error(self, status_code):
        """
        Error received
        :param status_code: Status Error Code
        :return:
        """
        logging.error('Twitter Error: %s' % str(status_code))


class TwitterUserStreamingListener(tweepy.StreamListener):

    def __init__(self, user):
        super(TwitterUserStreamingListener, self).__init__()
        self.user = user

    def on_status(self, tweet):
        """
        If new tweet is received, this function will be called.
        For each tweet will create a new Mongo Insert
        :param tweet:
        :return:
        """
        try:
            Connection.Instance().db.twitter.insert_one(
                {
                    'source': 'collector',
                    'data': {
                        'created_at': tweet.created_at,
                        'favorite_count': tweet.favorite_count,
                        'geo': tweet.geo,
                        'id': tweet.id,
                        'source': tweet.source,
                        'in_reply_to_screen_name': tweet.in_reply_to_screen_name,
                        'in_reply_to_status_id': tweet.in_reply_to_status_id,
                        'in_reply_to_user_id': tweet.in_reply_to_user_id,
                        'retweet_count': tweet.retweet_count,
                        'retweeted': tweet.retweeted,
                        'text': tweet.text,
                        'entities': tweet.entities
                    },
                    'user': self.user,
                    'created': what_time_is_it()
                })
        except Exception as e:
            logging.error("MongoDB Insert Error in listener: " + e)

    def on_error(self, status_code):
        """
        Error received
        :param status_code: Status Error Code
        :return:
        """
        logging.error('Twitter Error: %s' % str(status_code))
