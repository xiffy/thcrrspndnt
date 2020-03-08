import sqlite3
import requests
import os


class Unshorten:

    def __init__(self, url):
        self.conn = sqlite3.connect( os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'data/db.sqlite3'))
        self.shorturl = url
        self.curs = self.conn.cursor()
        self.get()

    def get(self):
        self.curs.execute("select * from unshorten where  shorturl = ?", (self.shorturl,))
        found = self.curs.fetchone()
        _, self.longurl = found if found else (None, None)

    def save(self, longurl):
        if not self.shorturl:
            return False
        if self.longurl:
            return False
        self.curs.execute("insert into unshorten (shorturl, longurl) values (?, ?)", (self.shorturl, longurl,))
        self.conn.commit()
        self.longurl = url


    @staticmethod
    def unshorten(short_url):
        cache = Unshorten(short_url)
        if cache.longurl:
            return cache.longurl
        result = requests.get(short_url)
        if not result.url == short_url:
            cache.save(result.url)
        return result.url



