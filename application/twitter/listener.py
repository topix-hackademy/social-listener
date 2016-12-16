import tweepy
import logging
from application.mongo import Connection


class TwitterStreamingListener(tweepy.StreamListener):

    def __init__(self):
        super(TwitterStreamingListener, self).__init__()

    def on_status(self, tweet):
        """
        If new tweet is received, this function will be called.
        For each tweet will create a new Mongo Insert
        :param tweet:
        :return:
        """
        Connection.Instance().insert('twitter',
                                     {
                                         "data": tweet._json,
                                         "hashtags": tweet.entities['hashtags']
                                     })

    def on_error(self, status_code):
        """
        Error received
        :param status_code: Status Error Code
        :return:
        """
        logging.error("Twitter Error: ", status_code)
