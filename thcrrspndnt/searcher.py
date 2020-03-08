from requests_oauthlib import OAuth1Session
import settings
from model.tweet import Tweet
from model.article import Article


class Searcher:

    def __init__(self):
        self.settings = settings.CONFIG['twitter']

    def harvest(self):
        twitter_session = OAuth1Session(self.settings['CONSUMER_KEY'],
                                        client_secret=self.settings['CONSUMER_SECRET'],
                                        resource_owner_key=self.settings['OAUTH_KEY'],
                                        resource_owner_secret=self.settings['OAUTH_SECRET'])
        result = twitter_session.get('https://api.twitter.com/1.1/search/tweets.json',
                                     params={'q': 'thecorrespondent.com',
                                             'count': 100,
                                             'result_type': 'recent'})
        tweets = result.json()
        for tweet in tweets['statuses']:
            parsed_tweet = Tweet.parse_json(tweet)
            if parsed_tweet:
                # it's up to the article to decide what to do with the found URL
                a = Article.maybe_find_or_create(parsed_tweet.corres_url)
                if a:
                    print("%s count: %s - %s" % (a.corry_id, a.tweetcount, a.title))



s = Searcher()
s.harvest()
