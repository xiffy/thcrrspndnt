from requests_oauthlib import OAuth1Session
import settings


class Tweeter:
    def __init__(self):
        self.settings = settings.CONFIG['twitter_post']

    def send_tweet(self, article):
        twitter_session = OAuth1Session(self.settings['CONSUMER_KEY'],
                                        client_secret=self.settings['CONSUMER_SECRET'],
                                        resource_owner_key=self.settings['OAUTH_KEY'],
                                        resource_owner_secret=self.settings['OAUTH_SECRET'])
        send = self.settings.get('SEND_TWEETS', True)
        if send:
            twitter_session.post('https://api.twitter.com/1.1/statuses/update.json',
                                 data={'status': "%s: %s - %s" % (article.author, article.title, article.share_url),
                                       'source': 'molecule.nl/thcrrspndnt',
                                       'callback_url': 'molecule.nl/'})
            print('Tweet sent for id: %s' % article.corry_id)