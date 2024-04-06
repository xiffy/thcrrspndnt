# -*- coding: utf-8 -*-
import json
import sqlite3

import settings
from .db import Db
from .unshorten import Unshorten
from .article import get_corry_id, searchquerybuilder
from urllib.parse import urlparse, urlunparse


class Tweet:
    def __init__(
        self, id=None, message=None, urls=None, corres_url=None, corry_id=None, db=None
    ):
        self.id = id
        self.message = message
        self.urls = json.dumps(urls) if urls else json.dumps({})
        self.corres_url = corres_url
        self.corry_id = corry_id
        self.db = db if db else Db()
        self.curs = self.db.conn.cursor()

    def __str__(self):
        return "url: %s - %s" % (self.corres_url, self.message)

    def get(self, id):
        self.curs.execute(
            "select id, message, urls, corres_url, corry_id from tweet where id = ?",
            (id,),
        )
        row = self.curs.fetchone()
        if row:
            self.id, self.message, self.urls, self.corres_url, self.corry_id = row
            self.urls = json.loads(self.urls)
            return self
        else:
            return False

    def insert(self):
        self.curs.execute(
            "insert into tweet (id, message, urls, corres_url, corry_id) values (?, ?, ?, ?, ?)",
            (
                self.id,
                self.message,
                self.urls,
                self.corres_url,
                get_corry_id(self.corres_url),
            ),
        )
        try:
            self.db.conn.commit()
        except sqlite3.OperationalError:
            print(f"Error while inserting tweet: {self.id}")
            self.db.conn.rollback()
            self.db.conn.close()
        return self

    def get_tweetcount_filtered(self, author=None):
        if not author:
            self.curs.execute("select count(id) from tweet")
        else:
            self.curs.execute(
                "select count(id) from article "
                "left join tweet on article.corry_id = tweet.corry_id "
                "where author = ?",
                (author,),
            )
        return self.curs.fetchone()[0]

    def get_tweetcount_searchquery(self, tokens):
        where, values = searchquerybuilder(tokens)
        self.curs.execute(
            "select count(id) from article "
            "left join tweet on article.corry_id = tweet.corry_id "
            "where %s " % " or ".join(where),
            values,
        )
        return self.curs.fetchone()[0]

    @staticmethod
    def find_urls(data):
        urls = []
        for word in data.split():
            parsed_url = urlparse(word)
            if parsed_url.scheme and parsed_url.netloc:
                urls.append(
                    urlunparse(
                        (
                            parsed_url.scheme,
                            parsed_url.netloc,
                            parsed_url.path.replace("…", ""),
                            None,
                            None,
                            None,
                        )
                    )
                )
        return urls

    def parse_csv(self, data):
        site = settings.CONFIG.get("site", "decorrespondent.nl")
        urls = self.find_urls(data["Content"])
        for url in urls:
            url = self.clean_url(url)
            if site not in url:
                url = Unshorten(db=self.db, url=url).as_class()
            if site in url:
                tweet_id = data["Tweet ID"].split(":")[1]
                cached = self.get(tweet_id)
                if not cached:
                    print(".", end="")
                    return Tweet(
                        id=tweet_id,
                        message=data.get("Content"),
                        urls=data.get("Tweet Link"),
                        corres_url=url,
                        db=self.db,
                    ).insert()
                return cached

    def clean_url(self, url):
        print(url)
        site = settings.CONFIG.get("site", "decorrespondent.nl")
        if site not in url:
            return url
        parsed_url = urlparse(url)
        path = parsed_url.path
        if len(parsed_url.path.split("/")) > 4:
            path = "/".join(parsed_url.path.split("/")[:4])
        print(path)
        netloc = parsed_url.netloc
        if "open" in parsed_url.netloc:
            netloc = site
        print("==> ", end="")
        print(urlunparse((parsed_url.scheme, netloc, path, None, None, None)))
        return urlunparse((parsed_url.scheme, netloc, path, None, None, None))

    @staticmethod
    def parse_json(data):
        site = settings.CONFIG.get("site", "thecorrespondent.com")
        urls = data["entities"].get("urls", None)
        corres_url = None
        if not urls:
            return False
        for url in urls:
            maybe_corry = url.get("expanded_url", None)
            if maybe_corry:
                if site not in maybe_corry:
                    maybe_corry = Unshorten.unshorten(maybe_corry)
                    if site in maybe_corry:
                        corres_url = maybe_corry
                        break
                else:
                    corres_url = maybe_corry
                    break

        if corres_url:
            cached = Tweet().get(data.get("id"))
            if not cached:
                print(".", end="")
                return Tweet(
                    id=data.get("id"),
                    message=data.get("text"),
                    urls=urls,
                    corres_url=corres_url,
                ).insert()
            return cached
        else:
            return False

    def parse_toot_json(self, data):
        corres_url = None
        site = settings.CONFIG.get("site", "decorrespondent.nl")
        if data.card and data.card.url:
            if site not in data.card.url:
                if site in Unshorten(db=self.db, url=data.card.url).as_class():
                    corres_url = data.card.url
            else:
                corres_url = data.card.url
        else:
            print("parse content")
        if corres_url:
            tweet = Tweet(db=self.db)
            cached = tweet.get(data.get("id"))
            if not cached:
                print(".", end="")
                return Tweet(
                    id=data.get("id"),
                    message=data.get("content"),
                    urls=[{"url": data.url, "uri": data.uri}],
                    corres_url=corres_url,
                    db=self.db,
                ).insert()
            return cached
        else:
            return False
