import tweepy


class TwitterInterface(object):

    def __init__(self, consumer_key, secret_key, access_token, secret_access_token, *args, **kwargs):
        self.auth = tweepy.OAuthHandler(consumer_key, secret_key)
        self.auth.set_access_token(access_token, secret_access_token)
        self.api = tweepy.API(self.auth)
        try:
            self.api.verify_credentials()
        except Exception:
            raise Exception("Authentication FAILED, please try with other credentials.")

