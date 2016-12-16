import tweepy
from application.twitter.listener.streaming import TwitterStreamingListener
from application.twitter.interface import TwitterInterface


class TwitterListener(TwitterInterface):

    def __init__(self, hashtags, *args, **kwargs):
        """
        Twitter Listener constructor. This class is used as middleware for the Twitter Listener
        :param hashtags: List of Hashtags / Words
        """
        super(TwitterListener, self).__init__(*args, **kwargs)
        self.hashtags = hashtags
        self.listener = TwitterStreamingListener()
        self.process_name = "Twitter Listener: <%s>" % "-".join(hashtags)
        self.stream = tweepy.streaming.Stream(self.auth, self.listener)

    def start(self, process_manager):
        """
        Create new Twitter Listener Process
        :param process_manager: Process Manager Instance
        :return:
        """
        try:
            process_manager.create_process(target=lambda: self.stream.filter(track=self.hashtags),
                                           name=self.process_name,
                                           ptype='twitter_listener')
        except Exception as e:
            raise e

    def __str__(self):
        """
        String representation
        :return:
        """
        return "Twitter Listener <{hashtags}>".format(hashtags=self.hashtags)
