import tweepy
from application.twitter.listener.streaming import TwitterStreamingListener, TwitterUserStreamingListener
from application.twitter.interface import TwitterInterface


class TwitterListener(TwitterInterface):

    def __init__(self, keywords, user, *args, **kwargs):
        """
        Twitter Listener constructor. This class is used as middleware for the Twitter Listener
        :param hashtags: List of Hashtags / Words
        """
        super(TwitterListener, self).__init__(*args, **kwargs)
        self.user = None
        self.hashtags = None

        if len(keywords[0]) > 0:
            self.keywords = keywords
            self.stream = tweepy.streaming.Stream(self.auth, TwitterStreamingListener(keywords))

        if len(user) > 0:
            try:
                self.user = self.api.get_user(user)
                self.user_stream = tweepy.streaming.Stream(self.auth, TwitterUserStreamingListener(user))
            except Exception as e:
                raise e

    def start(self, process_manager):
        """
        Create new Twitter Listener Process
        :param process_manager: Process Manager Instance
        :return:
        """
        if self.keywords:
            try:
                process_manager.create_process(target=lambda: self.stream.filter(track=self.keywords),
                                               name='Twitter Keywords Listener: <%s>' % '-'.join(self.keywords),
                                               ptype='twitter_listener')
            except Exception as e:
                raise e

        if self.user:
            try:
                process_manager.create_process(target=lambda: self.user_stream.filter(follow=[self.user.id_str]),
                                               name='Twitter User Listener: <%s>' % self.user.screen_name,
                                               ptype='twitter_listener')
            except Exception as e:
                raise e

    def __str__(self):
        """
        String representation
        :return:
        """
        return 'Twitter Listener'
