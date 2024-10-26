import requests
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from .db import Db
from tooter import Tooter


def searchquerybuilder(tokens):
    fields = ["title", "description", "author"]
    where = []
    values = []
    for field in fields:
        for token in tokens:
            where.append("{0} like ?".format(field))
            values.append("%{0}%".format(token.replace('"', "")))
    return (where, values)


class Article:
    def __init__(
        self,
        corry_id=None,
        share_url=None,
        title=None,
        author=None,
        created_at=None,
        published_at=None,
        description=None,
        tooted=False,
        db=None,
    ):
        self.corry_id = corry_id
        self.share_url = share_url
        self.title = title
        self.author = author
        self.created_at = created_at
        self.published_at = published_at
        self.description = description if description else ""
        self.tooted = tooted
        self.db = db if db else Db()
        self.curs = self.db.conn.cursor()

    def get(self, corry_id=None):
        self.curs.execute("select * from article where corry_id = ?", (corry_id,))
        row = self.curs.fetchone()
        if row:
            self.corry_id, self.share_url, self.title, self.author, self.created_at, self.published_at, self.description = (
                row
            )
            return self
        return False

    def insert(self):
        self.created_at = str(datetime.utcnow())
        self.curs.execute(
            "insert into article (corry_id, share_url, title, author, created_at, "
            "published_at, description)"
            "values (?, ?, ?, ?, ?, ?, ?)",
            (
                self.corry_id,
                self.share_url,
                self.title,
                self.author,
                self.created_at,
                self.published_at,
                self.description,
            ),
        )
        self.db.conn.commit()

    @property
    def tweetcount(self):
        self.curs.execute(
            "select count(id) from tweet where corry_id = ?", (self.corry_id,)
        )
        return self.curs.fetchone()[0]

    @property
    def nice_publish_date(self):
        return self.published_at[:10]

    def get_paged(self, start=0, amount=10):
        self.curs.execute(
            "select * from article order by published_at desc limit ?,?",
            (start, amount),
        )
        paged_rows = self.curs.fetchall()
        return [Article(*row) for row in paged_rows]

    def get_author_paged(self, author, start=0, amount=10):
        self.curs.execute(
            "select* from article where author = ? order by published_at desc limit ?,?",
            (author, start, amount),
        )
        paged_rows = self.curs.fetchall()
        return [Article(*row) for row in paged_rows]

    def get_count_filtered(self, author=None):
        if not author:
            self.curs.execute("select count(corry_id) from article")
        else:
            self.curs.execute(
                "select count(corry_id) from article where author = ?", (author,)
            )
        return self.curs.fetchone()[0]

    def get_searchcount(self, tokens):
        where, values = searchquerybuilder(tokens)
        self.curs.execute(
            "select count(*) from article where %s" % " or ".join(where), values
        )
        return self.curs.fetchone()[0]

    def get_search(self, tokens=None, start=0, amount=10):
        where, values = searchquerybuilder(tokens)
        values.append(start)
        values.append(amount)
        self.curs.execute(
            "select * from article where %s limit ?,?" % " or ".join(where), values
        )
        paged_rows = self.curs.fetchall()
        return [Article(*row) for row in paged_rows]

    @staticmethod
    def maybe_find_or_create(share_url=None):
        corry_id = get_corry_id(share_url)
        if not corry_id:
            return False
        cached = Article().get(corry_id=corry_id)
        if cached:
            return cached
        return Article().cache_article(share_url=share_url, corry_id=corry_id)

    def cache_article(self, share_url=None, corry_id=None):
        if not share_url.startswith("http"):
            print("Not a valid: URL: %s" % share_url)
            return None
        time.sleep(3)
        headers = {"User-Agent": "Chrome/Windows: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        result = requests.get(share_url, headers=headers)
        if result.status_code == 200:
            self.parse_article(result.content)
            if self.title:
                self.corry_id = corry_id
                self.share_url = share_url
                self.insert()
                print("\nNew article: %s - %s" % (self.corry_id, self.title))
                Tooter().send_toot(self)
                self.tooted = True
                return self
            else:
                print(result.content)
                return None
        else:
            print(f"Erreur: {result.status_code} - {share_url}")
            self.db.conn.rollback()
            return None

    def parse_article(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        for author in soup.findAll(attrs={"name": "author"}):
            self.author = author["content"]
        for desc in soup.findAll(attrs={"name":"description"}):
            self.description = desc["content"]
            break
        for meta in soup.findAll(
            property=[re.compile("og:.*"), re.compile("article:.*"), re.compile("twitter:.*")]
        ):
            prop = meta.attrs.get("property", None)
            value = meta.attrs.get("content", None)
            if prop == "twitter:title":
                self.title = value
            if prop == "article:published_time":
                self.published_at = value
        self.title = soup.find("title").text


def get_corry_id(url):
    path = urlparse(url)[2].split("/")
    if len(path) > 3 and path[1].isdigit():
        return path[1]
    else:
        return False
