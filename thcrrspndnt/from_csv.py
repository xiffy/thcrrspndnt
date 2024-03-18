import csv
import settings
from model.tweet import Tweet
from model.article import Article


with open(settings.CONFIG["tweets_csv"], newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for count, row in enumerate(reader):
        if count == 0:
            print(row.keys())
        if "decorrespondent.nl" in row["Content"]:
            print(row["Content"])
            parsed_status = Tweet().parse_csv(row)
            if parsed_status:
                article = Article.maybe_find_or_create(parsed_status.corres_url)
                if article and article.tooted:
                    break
