import sqlite3

import requests
from .db import Db


class Unshorten:
    def __init__(self, url):
        self.db = Db()
        self.curs = self.db.conn.cursor()
        self.shorturl = url
        self.longurl = None
        if url:
            self.get()

    def get(self):
        self.curs.execute(
            "select * from unshorten where  shorturl = ?", (self.shorturl,)
        )
        found = self.curs.fetchone()
        _, self.longurl = found if found else (None, None)

    def save(self, longurl):
        if not longurl:
            print("No longurl")
            return False
        if not self.shorturl:
            return False
        if self.longurl:
            return False
        self.curs.execute(
            "insert into unshorten (shorturl, longurl) values (?, ?)",
            (self.shorturl, longurl),
        )
        try:
            self.db.conn.commit()
        except sqlite3.OperationalError:
            print(f"Not inserted: {self.shorturl} => {longurl}")
            self.db.conn.rollback()
        self.longurl = longurl

    def as_class(self):
        if self.longurl:
            return self.longurl
        result = requests.get(self.shorturl)
        if result.url and result.url != self.shorturl:
            self.save(result.url)
        return result.url

    @staticmethod
    def unshorten(short_url):
        print(short_url)
        if "http" not in short_url:
            return None
        cache = Unshorten(short_url)
        if cache.longurl:
            return cache.longurl
        result = requests.get(short_url)
        if not result.url == short_url:
            cache.save(result.url)
        return result.url
