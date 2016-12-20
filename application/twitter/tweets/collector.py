from application.mongo import Connection
from application.twitter.interface import TwitterInterface
from application.twitter.tweets.fetcher import TweetsFetcher
from application.processmanager import ProcessManager
from application.utils.helpers import what_time_is_it
import logging


class TweetCollector(TwitterInterface):

    def __init__(self, user, *args, **kwargs):
        """
        Twitter Collector. This class is used for retrieve tweets from a specific user
        """
        super(TweetCollector, self).__init__(*args, **kwargs)
        self.user = user
        self.process_name = "Tweets Collector: <%s>" % user
        self.fetcherInstance = TweetsFetcher(self.auth, self.user, self.process_name)

    def __str__(self):
        """
        String representation
        :return:
        """
        return "Tweet Collector for user <{user}>".format(user=self.user)

    def start(self, process_manager):
        """
        Start async job for user's tweets
        :param process_manager: Process manager instance
        :return:
        """
        try:
            process_manager.create_process(target=self.fetcher,
                                           name=self.process_name,
                                           ptype='twitter_collector')
        except Exception as e:
            raise e

    def fetcher(self):
        """
        Tweets loader
        :return:
        """
        for page in self.fetcherInstance.get_tweets():
            for tweet in page:
                try:
                    Connection.Instance().insert('twitter', 'collector',
                                                 {
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
                                                     'user': tweet.user.screen_name,
                                                     'created': what_time_is_it()
                                                 })
                except Exception as e:
                    logging.error("MongoDB Insert Error: " + e)
        import multiprocessing
        ProcessManager.terminate_process(multiprocessing.current_process().pid, True)
