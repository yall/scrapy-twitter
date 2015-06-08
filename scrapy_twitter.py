# coding:utf-8

from scrapy import log
from scrapy.http import Request, Response

import twitter


class TwitterUserTimelineRequest(Request):

    def __init__(self, *args, **kwargs):
        self.screen_name = kwargs.pop('screen_name', None)
        self.count = kwargs.pop('count', None)
        self.max_id = kwargs.pop('max_id', None)
        super(TwitterUserTimelineRequest, self).__init__('http://twitter.com',
                                                         dont_filter=True,
                                                         **kwargs)


class TwitterStreamFilterRequest(Request):

    def __init__(self, *args, **kwargs):
        self.track = kwargs.pop('track', None)
        super(TwitterStreamFilterRequest, self).__init__('http://twitter.com',
                                                         dont_filter=True,
                                                         **kwargs)


class TwitterResponse(Response):

    def __init__(self, *args, **kwargs):
        self.tweets = kwargs.pop('tweets', None)
        super(TwitterResponse, self).__init__('http://twitter.com',
                                              *args,
                                              **kwargs)


class TwitterDownloaderMiddleware(object):

    def __init__(self,
                 consumer_key, consumer_secret,
                 access_token_key, access_token_secret):
        self.api = twitter.Api(consumer_key=consumer_key,
                               consumer_secret=consumer_secret,
                               access_token_key=access_token_key,
                               access_token_secret=access_token_secret)
        log.msg('Using creds [CONSUMER KEY: %s, ACCESS TOKEN KEY: %s]' %
                (consumer_key, access_token_key),
                level=log.INFO)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        consumer_key = settings['TWITTER_CONSUMER_KEY']
        consumer_secret = settings['TWITTER_CONSUMER_SECRET']
        access_token_key = settings['TWITTER_ACCESS_TOKEN_KEY']
        access_token_secret = settings['TWITTER_ACCESS_TOKEN_SECRET']
        return cls(consumer_key,
                   consumer_secret,
                   access_token_key,
                   access_token_secret)

    def process_request(self, request, spider):

        if isinstance(request, TwitterUserTimelineRequest):
            tweets = self.api.GetUserTimeline(screen_name=request.screen_name,
                                              count=request.count,
                                              max_id=request.max_id)
            return TwitterResponse(tweets=[tweet.AsDict() for tweet in tweets])

        if isinstance(request, TwitterStreamFilterRequest):
            tweets = self.api.GetStreamFilter(track=request.track)
            return TwitterResponse(tweets=tweets)

    def process_response(self, request, response, spider):
        return response


from scrapy.item import DictItem, Field


def to_item(dict_tweet):
    field_list = dict_tweet.keys()
    fields = {field_name: Field() for field_name in field_list}
    item_class = type('TweetItem', (DictItem,), {'fields': fields})
    return item_class(dict_tweet)
