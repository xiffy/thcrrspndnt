from mastodon import Mastodon
import settings
import datetime
from model.tweet import Tweet
from model.article import Article


class MastoSearch:
    def __init__(self):
        self.search_query = settings.CONFIG["query"]
        self.mastodon = Mastodon(access_token=settings.CONFIG["access_token"], api_base_url="https://mastodon.nl/", )

    def harvest(self):
        for query in self.search_query:
            print(query)
            response = self.mastodon.search(query, result_type="statuses")
            for status in response["statuses"]:
                parsed_status = Tweet.parse_toot_json(status)
                if parsed_status:
                    Article.maybe_find_or_create(parsed_status.corres_url)


def main():
    m = MastoSearch()
    m.harvest()


if __name__ == "__main__":
    main()
