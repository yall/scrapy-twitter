# coding:utf-8

from scrapy import log
from scrapy.http import Request, Response

import twitter

"""
Twitter Request Subclasses
"""

class TwitterUserTimelineRequest(Request):
    
    def __init__(self, *args, **kwargs):
    	self.screen_name = kwargs.pop('screen_name', None)
    	self.count       = kwargs.pop('count', None)
    	self.max_id      = kwargs.pop('max_id', None)
        super(TwitterUserTimelineRequest, self).__init__('http://twitter.com', dont_filter = True, **kwargs)

class TwitterStreamFilterRequest(Request):
    
    def __init__(self, *args, **kwargs):
    	self.screen_name = kwargs.pop('track', None)
        super(TwitterStreamFilterRequest, self).__init__('http://twitter.com', dont_filter = True, **kwargs)


"""
Twitter Response Subclasses
"""

class TwitterResponse(Response):
    
    def __init__(self, *args, **kwargs):
    	self.tweets = kwargs.pop('tweets', None)
        super(TwitterResponse, self).__init__('http://twitter.com', *args, **kwargs)

"""
Twitter DownloaderMiddlerware
"""

class TwitterDownloaderMiddleware(object):

	def __init__(self, settings):
		self.api = twitter.Api(
			consumer_key = 			settings['TWITTER_CONSUMER_KEY'],
			consumer_secret = 		settings['TWITTER_CONSUMER_SECRET'],
			access_token_key = 		settings['TWITTER_ACCESS_TOKEN_KEY'],
			access_token_secret = 	settings['TWITTER_ACCESS_TOKEN_SECRET'])

	@classmethod
	def from_crawler(cls, crawler):
	    return cls(crawler.settings)

	def process_request(self, request, spider):
		tweets = self.api.GetUserTimeline(
						screen_name=request.screen_name,
						count=request.count,
						max_id=request.max_id)

		return TwitterResponse(tweets = tweets)

	def process_response(self, request, response, spider):
		return response

from scrapy.item import DictItem, Field


"""
Utility methods
"""

def to_item(tweet):
	dict_tweet = tweet.AsDict()
	field_list = dict_tweet.keys()
	fields = {field_name: Field() for field_name in field_list}
	item_class = type('TweetItem', (DictItem,), {'fields': fields})
	return item_class(dict_tweet)