import tweepy
import time
import logging


class TweetFollower(object):

    def __init__(self, auth, user, process_name):
        """
        Class constructor
        :param auth: Tweepy Auth object
        :param user: User to search
        :param process_name: Name of the process to create
        """
        self.api = tweepy.API(auth)
        self.process_name = process_name
        try:
            self.user = self.api.get_user(user)
        except Exception as e:
            raise e
        self.user_cursor = tweepy.Cursor(self.api.followers, screen_name=user)

    def get_followers(self):
        while True:
            try:
                yield self.user_cursor.pages().next()
            except tweepy.RateLimitError:
                logging.info("[%s] Timeout Reached, Sleep for 15 minutes before restart" % self.process_name)
                time.sleep(15 * 60)
                logging.info("[%s] Waking up. Try again" % self.process_name)
            except StopIteration:
                logging.info("[%s] Stop Iteration, process complete" % self.process_name)
                break
            except Exception as e:
                logging.info("[%s] Generic Error, restart in 60 seconds: %s" % (self.process_name, e))
                time.sleep(60)
