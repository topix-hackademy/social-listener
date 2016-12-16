import logging
from application.mongo import Connection
from application.twitter.interface import TwitterInterface
from application.twitter.tweets.fetcher import TweetsFetcher


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
                logging.info(tweet)
                # TODO: Insert To MONGODB
        # TODO: Process is finished, I want to set some flag to say "Hey, we are done! :)"
