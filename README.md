# scrapy-twitter

A lightweight wrapper over python-twitter library to use it in scrapy projects.

## Usage

Install

    sudo pip install -e git+https://github.com/yall/scrapy-twitter.git#egg=scrapy_twitter

Set your API credentials and add TwitterDownloaderMiddleware in your scrapy project settings

```python
DOWNLOADER_MIDDLEWARES = { 
    'scrapy_twitter.TwitterApiDownloaderMiddleware': 10,
}
TWITTER_CONSUMER_KEY        = 'xxxx'
TWITTER_CONSUMER_SECRET     = 'xxxx'
TWITTER_ACCESS_TOKEN_KEY    = 'xxxx'
TWITTER_ACCESS_TOKEN_SECRET = 'xxxx'
```

## Spider examples


### User Timeline

This spider get all tweets of a user timeline, iterating with max_id while there are remaining tweets.

    scrapy crawl user-timeline -a screen_name=zachbraff -o zb_tweets.json

```python
import scrapy

from scrapy_twitter import TwitterUserTimelineRequest, to_item

class UserTimelineSpider(scrapy.Spider):
    name = "user-timeline"
    allowed_domains = ["twitter.com"]

    def __init__(self, screen_name = None, *args, **kwargs):
        if not screen_name:
            raise scrapy.exceptions.CloseSpider('Argument scren_name not set.')
        super(UserTimelineSpider, self).__init__(*args, **kwargs)
        self.screen_name = screen_name
        self.count = 100

    def start_requests(self):
        return [ TwitterUserTimelineRequest(
                    screen_name = self.screen_name, 
                    count = self.count) ]

    def parse(self, response):
        tweets = response.tweets

        for tweet in tweets:
            yield to_item(tweet)

        if tweets:
            yield TwitterUserTimelineRequest(
                    screen_name = self.screen_name, 
                    count = self.count,
                    max_id = tweets[-1].id - 1) 
```

### Streaming

This spider plugs to the streaming API and triggers all tweets to the pipeline.

    scrapy crawl stream-filter -a track=#starwars

```python
import scrapy

from scrapy_twitter import TwitterStreamFilterRequest, to_item

class StreamFilterSpider(scrapy.Spider):
    name = "stream-filter"
    allowed_domains = ["twitter.com"]

    def __init__(self, track = None, *args, **kwargs):
        if not track:
            raise scrapy.exceptions.CloseSpider('Argument track not set.')
        super(StreamFilterSpider, self).__init__(*args, **kwargs)
        self.track = track

    def start_requests(self):
        return [ TwitterStreamFilterRequest(track = self.track) ]

    def parse(self, response):
        for tweet in response.tweets:
            yield to_item(tweet)
```