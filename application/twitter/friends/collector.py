from application.twitter.interface import TwitterInterface
import logging
from application.processmanager import ProcessManager
from application.utils.helpers import what_time_is_it
from application.twitter.friends.friends import TweetFriends
from application.mongo import Connection


class FriendsCollector(TwitterInterface):

    def __init__(self, user, *args, **kwargs):
        """
        Friends Collector. This class is used for retrieve friends of a specific user
        """
        super(FriendsCollector, self).__init__(*args, **kwargs)
        self.user = user
        self.process_name = "Friends of user: <%s>" % user
        self.fetcherInstance = TweetFriends(self.auth, self.user, self.process_name)

    def __str__(self):
        """
        String representation
        :return:
        """
        return "Friends Collector for user <{user}>".format(user=self.user)

    def start(self, process_manager):
        """
        Start async job for user's friends
        :param process_manager: Process manager instance
        :return:
        """
        try:
            process_manager.create_process(target=self.fetcher,
                                           name=self.process_name,
                                           ptype='twitter_follower')
        except Exception:
            raise Exception('Error Creating new Process')

    def fetcher(self):
        """
        Friends loader
        :return:
        """
        for friend in self.fetcherInstance.get_friends():
            try:
                if not Connection.Instance().db.twitter.find_one({'source': 'friends',
                                                                  'user': self.user,
                                                                  'data.userid': friend.id}):
                    Connection.Instance().db.twitter.insert_one({
                        'source': 'friends',
                        'data': {
                            'userid': friend.id,
                            'description': friend.description,
                            'favourites_count': friend.favourites_count,
                            'followers_count': friend.followers_count,
                            'friends_count': friend.friends_count,
                            'lang': friend.lang,
                            'location': friend.location,
                            'name': friend.name,
                            'screen_name': friend.screen_name,
                            'geo_enabled': friend.geo_enabled,
                            'url': friend.url,
                            'time_zone': friend.time_zone,
                            'statuses_count': friend.statuses_count
                        },
                        'user': self.user,
                        'created': what_time_is_it()
                    })
            except Exception as e:
                logging.error("MongoDB Insert Error in get friends: " + e.message)
        import multiprocessing
        ProcessManager.terminate_process(multiprocessing.current_process().pid, True)
