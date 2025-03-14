import settings
from model.db import Db
from model.unshorten import Unshorten

from model.article import Article


site = settings.CONFIG.get("site", "decorrespondent.nl")
urls = []
with open(settings.CONFIG["urllist"]) as urllist:
    urls = [line.rstrip() for line in urllist]

for url in urls:
    if site not in url:
        url = Unshorten(url)
    if site in url:
        print(url)
        article = Article.maybe_find_or_create(url)
    else:
        print("Noooooooooooooooooooooooooooooooo!", url)
