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


class TwitterInterface(object):

    def __init__(self, consumer_key, secret_key, access_token, secret_access_token, hashtags):
        """
        Twitter Interface constructor. This class is used as an interface to the Twitter Listener
        :param consumer_key: Check Out Twitter Documentation
        :param secret_key: Check Out Twitter Documentation
        :param access_token: Check Out Twitter Documentation
        :param secret_access_token: Check Out Twitter Documentation
        :param hashtags: List of Hashtags / Words
        """
        self.auth = tweepy.OAuthHandler(consumer_key, secret_key)
        self.auth.set_access_token(access_token, secret_access_token)
        self.listener = TwitterStreamingListener()
        self.hashtags = hashtags
        self.process_name = "Twitter: " + "-".join(hashtags)
        self.stream = tweepy.streaming.Stream(self.auth, self.listener)

    def test_auth(self):
        """
        Simple Function used to check if authorization object is valid or not
        :return: True / False
        """
        try:
            tweepy.API(self.auth).rate_limit_status()
        except Exception as e:
            logging.error("Error trying to connect the object: " + str(self))
            logging.error(e)
            return False
        return True

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
