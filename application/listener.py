import tweepy
import logging
from application.mongo import Connection


class TwitterStreamingListener(tweepy.StreamListener):
    def __init__(self):
        super(TwitterStreamingListener, self).__init__()

    def on_status(self, tweet):
        logging.info("Inserting: " + tweet.text)
        Connection.Instance().insert('twitter',
                                     {
                                         "data": tweet._json,
                                         "hashtags": tweet.entities['hashtags']
                                     })

    def on_error(self, status_code):
        logging.error("Twitter Error: ", status_code)


class TwitterInterface(object):

    def __init__(self, consumer_key, secret_key, access_token, secret_access_token, hashtags):
        self.auth = tweepy.OAuthHandler(consumer_key, secret_key)
        self.auth.set_access_token(access_token, secret_access_token)
        self.listener = TwitterStreamingListener()
        self.hashtags = hashtags
        self.process_name = "Twitter: " + "-".join(hashtags)
        self.stream = tweepy.streaming.Stream(self.auth, self.listener)

    def test_auth(self):
        try:
            tweepy.API(self.auth).rate_limit_status()
        except Exception as e:
            print e
            logging.error("Error trying to connect the object: " + str(self))
            return False
        return True

    def start(self, process_manager):
        process_manager.create_process(target=lambda: self.stream.filter(track=self.hashtags),
                                       name=self.process_name)

    def __str__(self):
        return "Twitter Interface <{hashtags}>".format(auth=self.auth,
                                                               hashtags=self.hashtags)
