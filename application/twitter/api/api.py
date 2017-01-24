from application.mongo import Connection
from flask import jsonify


class APIManager(object):
    
    @staticmethod
    def index():
        """
        API Manager Index Page
        :return:
        """
        return jsonify(
            status=200,
            detail="Welcome to Social Manager API",
            services=[{"source": "Twitter", "url": "/api/v1/twitter"}]
        ), 200


class TwitterAPI(object):
    
    @staticmethod
    def index():
        """
        Twitter API Index Page
        :return:
        """
        return jsonify(
            status=200,
            detail="Twitter API Index",
            services=[
                {
                    "name": "Listener",
                    "url": "/api/v1/twitter/search/{KEYWORD-TO-SEARCH}",
                    "util": "/api/v1/twitter/keywords"
                },
                {
                    "name": "Tweet Discover",
                    "url": "/api/v1/twitter/tweet/{USER-TO-DISCOVER}",
                    "util": "/api/v1/twitter/users"
                },
                {
                    "name": "Friends Discover",
                    "url": "/api/v1/twitter/friends/{USER-TO-DISCOVER}",
                    "util": "/api/v1/twitter/users"
                },
                {
                    "name": "Follower Discover",
                    "url": "/api/v1/twitter/followers/{USER-TO-DISCOVER}",
                    "util": "/api/v1/twitter/users"
                }
            ]
        ), 200
    
    @staticmethod
    def get_keywords():
        """
        Return the list of all available keywords
        :return: Json
        """
        return jsonify(status=200,
                       keywords=Connection.Instance().db.twitter.find({"source": "listener"}).distinct("keywords")), 200
    
    @staticmethod
    def search(keyword, page=1):
        """
        Get all tweets from a given keyword with pagination support.
        :param keyword: Keyword to search
        :param page: Page Number
        :return:
        """
        page = int(page) if int(page) > 0 else 1
        n_result = 10
        total_result = Connection.Instance().db.twitter.find({"keywords": keyword, "source": "listener"}).count()
        result = list(Connection.Instance().db.twitter.find(
            {
                "keywords": keyword,
                "source": "listener"
            },
            {
                "_id": False,
                "created": False,
                "keywords": False,
                "source": False
            }).skip((page-1)*n_result).limit(n_result))
        
        page_size = len(result)
        
        return jsonify(
            total_result=total_result,
            status=200,
            page_size=page_size,
            page=page,
            result=[data['data'] for data in result],
            next="/api/v1/twitter/search/python/%s" % str(page + 1) if page_size == n_result else None,
            before="/api/v1/twitter/search/python/%s" % str(page - 1) if page > 1 else None
        ), 200

    @staticmethod
    def get_users():
        """
        Return list of users fetched
        :return: Json
        """
        return jsonify(status=200,
                       users=Connection.Instance().db.twitter.find({"user": {"$ne": None}}).distinct("user")), 200

    @staticmethod
    def get_tweets(user, page=1):
        """
        Return List of tweets from a specific user
        :param user: User Screen Name
        :param page: Page Number
        :return:
        """
        total_result = Connection.Instance().db.twitter.find({"user": user, "source": "collector"}).count()
        page = int(page) if int(page) > 0 else 1
        n_result = 10
        result = list(Connection.Instance().db.twitter.find(
            {
                "source": "collector",
                "user": user
            }
        ).skip((page-1)*n_result).limit(n_result))
        
        page_size = len(result)

        return jsonify(
            total_result=total_result,
            status=200,
            page_size=page_size,
            page=page,
            result=[data['data'] for data in result],
            next="/api/v1/twitter/tweets/%s/%s" % (user, str(page + 1)) if page_size == n_result else None,
            before="/api/v1/twitter/tweets/%s/%s" % (user, str(page - 1)) if page > 1 else None
        ), 200

    @staticmethod
    def get_followers(user, page=1):
        """
        Return List of followers of a specific user
        :param user: User Screen Name
        :param page: Page Number
        :return:
        """
        total_result = Connection.Instance().db.twitter.find({"user": user, "source": "follower"}).count()
        page = int(page) if int(page) > 0 else 1
        n_result = 10
        result = list(Connection.Instance().db.twitter.find(
            {
                "source": "follower",
                "user": user
            }
        ).skip((page - 1) * n_result).limit(n_result))

        page_size = len(result)

        return jsonify(
            total_result=total_result,
            status=200,
            page_size=page_size,
            page=page,
            result=[data['data'] for data in result],
            next="/api/v1/twitter/followers/%s/%s" % (user, str(page + 1)) if page_size == n_result else None,
            before="/api/v1/twitter/followers/%s/%s" % (user, str(page - 1)) if page > 1 else None
        ), 200

    @staticmethod
    def get_friends(user, page=1):
        """
        Return List of friends of a specific user
        :param user: User Screen Name
        :param page: Page Number
        :return:
        """
        total_result = Connection.Instance().db.twitter.find({"user": user, "source": "friends"}).count()
        page = int(page) if int(page) > 0 else 1
        n_result = 10
        result = list(Connection.Instance().db.twitter.find(
            {
                "source": "friends",
                "user": user
            }
        ).skip((page - 1) * n_result).limit(n_result))
    
        page_size = len(result)
    
        return jsonify(
            total_result=total_result,
            status=200,
            page_size=page_size,
            page=page,
            result=[data['data'] for data in result],
            next="/api/v1/twitter/friends/%s/%s" % (user, str(page + 1)) if page_size == n_result else None,
            before="/api/v1/twitter/friends/%s/%s" % (user, str(page - 1)) if page > 1 else None
        ), 200
