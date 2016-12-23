from application.twitter.interface import TwitterInterface
import logging
from application.processmanager import ProcessManager
from application.utils.helpers import what_time_is_it
from application.twitter.follower.follower import TweetFollower
from application.mongo import Connection


class FollowerCollector(TwitterInterface):

    def __init__(self, user, *args, **kwargs):
        """
        Twitter Collector. This class is used for retrieve followers of a specific user
        """
        super(FollowerCollector, self).__init__(*args, **kwargs)
        self.user = user
        self.process_name = "Follower of user: <%s>" % user
        self.fetcherInstance = TweetFollower(self.auth, self.user, self.process_name)

    def __str__(self):
        """
        String representation
        :return:
        """
        return "Follower Collector for user <{user}>".format(user=self.user)

    def start(self, process_manager):
        """
        Start async job for user's followers
        :param process_manager: Process manager instance
        :return:
        """
        try:
            process_manager.create_process(target=self.fetcher,
                                           name=self.process_name,
                                           ptype='twitter_follower')
        except Exception as e:
            raise Exception('Error Creating new Process')

    def fetcher(self):
        """
        Followers loader
        :return:
        """
        for page in self.fetcherInstance.get_followers():
            for follower in page:
                try:
                    Connection.Instance().db.twitter.insert_one({
                        'source': 'follower',
                        'data': {
                            'userid': follower.id,
                            'description': follower.description,
                            'favourites_count': follower.favourites_count,
                            'followers_count': follower.followers_count,
                            'friends_count': follower.friends_count,
                            'lang': follower.lang,
                            'location': follower.location,
                            'name': follower.name,
                            'screen_name': follower.screen_name,
                            'geo_enabled': follower.geo_enabled,
                            'url': follower.url,
                            'time_zone': follower.time_zone,
                            'statuses_count': follower.statuses_count
                        },
                        'user': self.user,
                        'created': what_time_is_it()
                    })
                except Exception as e:
                    logging.error("MongoDB Insert Error in get followers: " + e)
        import multiprocessing
        ProcessManager.terminate_process(multiprocessing.current_process().pid, True)
