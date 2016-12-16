import logging

import tweepy
from application.mongo import Connection
from application.twitter.listener.interface import TwitterInterface


class TwitterListener(TwitterInterface):

    def __init__(self, hashtags, *args, **kwargs):
        """
        Twitter Listener constructor. This class is used as middleware for the Twitter Listener
        :param hashtags: List of Hashtags / Words
        """
        super(TwitterListener, self).__init__(*args, **kwargs)
        self.hashtags = hashtags
        self.listener = TwitterStreamingListener()
        self.process_name = "Twitter: " + "-".join(hashtags)
        self.stream = tweepy.streaming.Stream(self.auth, self.listener)

    def start(self, process_manager):
        """
        Create new Twitter Listener Process
        :param process_manager: Process Manager Instance
        :return:
        """
        process_manager.create_process(target=lambda: self.stream.filter(track=self.hashtags),
                                       name=self.process_name)

    def __str__(self):
        """
        String representation
        :return:
        """
        return "Twitter Interface <{hashtags}>".format(auth=self.auth,
                                                       hashtags=self.hashtags)


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
