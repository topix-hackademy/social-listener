import tweepy
import logging

class TwitterStreamingListener(tweepy.StreamListener):
    def __init__(self):
        super(TwitterStreamingListener, self).__init__()

    def on_status(self, status):
        # automatic called when a new tweet is received
        logging.info(status.text)

    def on_error(self, status_code):
        # automatic called when an error occures
        logging.error("Twitter Error: ", status_code)

class TwitterInterface(object):

    def __init__(self, CONSUMER_KEY, SECRET_KEY, ACCESS_TOKEN, SECRET_ACCESS_TOKEN, hashtags):
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY, SECRET_KEY)
        self.auth.set_access_token(ACCESS_TOKEN, SECRET_ACCESS_TOKEN)
        self.listener = TwitterStreamingListener()
        self.hashtags = hashtags
        self.process_name = "Twitter: " + "-".join(hashtags)
        self.stream = tweepy.streaming.Stream(self.auth, self.listener)

    def start(self, process_manager):
        process_manager.create_process(target=lambda: self.stream.filter(track=self.hashtags),
                                       name=self.process_name)
