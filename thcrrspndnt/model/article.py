import sqlite3
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from .db import Db


class Article:

    def __init__(self, corry_id=None, share_url=None, title=None, author=None, created_at=None, published_at=None):
        self.corry_id = corry_id
        self.share_url = share_url
        self.title = title
        self.author = author
        self.created_at = created_at
        self.published_at = published_at
        self.db = Db()
        self.curs = self.db.conn.cursor()

    def get(self, corry_id=None):
        self.curs.execute("select * from article where corry_id = ?", (corry_id,))
        row = self.curs.fetchone()
        if row:
            self.corry_id, self.share_url, self.title, self.author, self.created_at,\
                self.published_at = row
            return self
        return False

    def insert(self):
        self.created_at = str(datetime.utcnow())
        self.curs.execute("insert into article (corry_id, share_url, title, author, created_at, published_at)"
                          "values (?, ?, ?, ?, ?, ?)", (self.corry_id, self.share_url, self.title,
                                                        self.author, self.created_at, self.published_at,))
        self.db.conn.commit()

    @property
    def tweetcount(self):
        self.curs.execute("select count(id) from tweet where corry_id = ?", (self.corry_id,))
        return self.curs.fetchone()[0]

    def get_paged(self):
        self.curs.execute("select * from article order by created_at desc ")
        all = self.curs.fetchall()
        return [Article(*row) for row in all]

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
        result = requests.get(share_url)
        if result.status_code == 200:
            self.parse_article(result.content)
            if self.title:
                self.corry_id = corry_id
                self.share_url = share_url
                self.insert()
                return self

    def parse_article(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        for author in soup.findAll(attrs={'name': 'author'}):
            self.author = author['content']
        for meta in soup.findAll(property=[re.compile('og:.*'), re.compile('article:.*')]):
            prop = meta.attrs.get('property', None)
            value = meta.attrs.get('content', None)
            if prop == 'og:title':
                self.title = value
            if prop == 'article:published_time':
                self.published_at = value




def get_corry_id(url):
    path = urlparse(url)[2].split('/')
    if len(path) > 3 and path[1].isdigit():
        return path[1]
    else:
        return False
