from mastodon import Mastodon
import settings
from datetime import datetime
from model.db import Db
from model.tweet import Tweet
from model.article import Article


class MastoSearch:
    def __init__(self):
        self.search_query = settings.CONFIG["query"]
        self.mastodon = Mastodon(
            access_token=settings.CONFIG["access_token"],
            api_base_url="https://mastodon.nl/",
            version_check_mode="none",
        )
        self.db = Db()

    def harvest(self):
        for query in self.search_query:
            print(f"\n{datetime.now()}: searching| ", end="")
            response = self.mastodon.search(query, result_type="statuses")
            for status in response["statuses"]:
                tweet = Tweet(db=self.db)
                parsed_status = tweet.parse_toot_json(status)
                if parsed_status:
                    Article.maybe_find_or_create(parsed_status.corres_url)


def main():
    m = MastoSearch()
    m.harvest()


if __name__ == "__main__":
    main()
