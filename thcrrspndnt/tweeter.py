import settings
from requests_oauthlib import OAuth1Session


class Tweeter:
    def __init__(self):
        self.settings = settings.CONFIG['twitter_post']

    def send_tweet(self, article):
        twitter_session = OAuth1Session(self.settings['CONSUMER_KEY'],
                                        client_secret=self.settings['CONSUMER_SECRET'],)
        send = self.settings.get('SEND_TWEETS', True)
        if send:

            # twitter_session.post('https://api.twitter.com/1.1/statuses/update.json',
            #                      data={'text': "%s: %s - %s" % (article.author, article.title, article.share_url),
            #                            'source': 'molecule.nl/thcrrspndnt',
            #                            'callback_url': 'molecule.nl/'})
            # print('Tweet, tweet, tweet, tweet, yeah! sent for id: %s' % article.corry_id)

            # resource_owner_key = token.get("oauth_token")
            # resource_owner_secret = token.get("oauth_token_secret")
            # print("Got OAuth token: %s" % resource_owner_key)
            #
            # # Get authorization
            # base_authorization_url = "https://api.twitter.com/oauth/authorize"
            # authorization_url = twitter_session.authorization_url(base_authorization_url)
            # print("Please go here and authorize: %s" % authorization_url)
            # verifier = input("Paste the PIN here: ")
            #
            # # Get the access token
            # access_token_url = "https://api.twitter.com/oauth/access_token"
            # oauth = OAuth1Session(
            #     self.settings["CONSUMER_KEY"],
            #     client_secret=self.settings["CONSUMER_SECRET"],
            #     resource_owner_key=resource_owner_key,
            #     resource_owner_secret=resource_owner_secret,
            #     verifier=verifier,
            # )
            # oauth_tokens = oauth.fetch_access_token(access_token_url)
            #
            # access_token = oauth_tokens["oauth_token"]
            # access_token_secret = oauth_tokens["oauth_token_secret"]
            # print(oauth_tokens)
            # Make the request
            oauth = OAuth1Session(
                self.settings["CONSUMER_KEY"],
                client_secret=self.settings["CONSUMER_SECRET"],
                resource_owner_key=self.settings["OAUTH_KEY"],
                resource_owner_secret=self.settings["OAUTH_SECRET"],
            )
            payload = {"text": "%s: %s - %s" % (article.author, article.title, article.share_url),
                       'source': 'molecule.nl/thcrrspndnt',
                       }

            # Making the request
            response = oauth.post(
                "https://api.twitter.com/2/tweets",
                json=payload,
            )
def main():
    t = Tweeter()
    t.send_tweet("Check")


if __name__ == "__main__":
    main()