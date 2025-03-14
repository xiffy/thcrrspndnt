import settings
from model.db import Db
from model.article import Article


site = settings.CONFIG.get("site", "decorrespondent.nl")
urls = []
with open(settings.CONFIG["urllist"]) as urllist:
    urls = [line.rstrip() for line in urllist]

for url in urls:
    if site in url:
        article = Article.maybe_find_or_create(url)
