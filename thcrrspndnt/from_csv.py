import csv
import settings
from model.db import Db
from model.tweet import Tweet
from model.article import Article


with open(settings.CONFIG["tweets_csv"], newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    db = Db()
    for count, row in enumerate(reader):
        #  if "decorrespondent.nl" in row["Content"]:
        tweet = Tweet(db=db)
        parsed_status = tweet.parse_csv(row)
        if parsed_status:
            article = Article.maybe_find_or_create(parsed_status.corres_url)
