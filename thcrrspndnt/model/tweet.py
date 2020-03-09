import sqlite3
import json
import os
from .db import Db
from .unshorten import Unshorten
from .article import get_corry_id


class Tweet:

    def __init__(self, id=None, message=None, urls=None, corres_url=None, corry_id=None):
        self.id = id
        self.message = message
        self.urls = urls if urls else {}
        self.corres_url = corres_url
        self.corry_id = corry_id
        self.db = Db()
        self.curs = self.db.conn.cursor()

    def __str__(self):
        return "url: %s - %s" % (self.corres_url, self.message)

    def get(self, id):
        self.curs.execute('select id, message, urls, corres_url, corry_id from tweet where id = ?', (id,))
        row = self.curs.fetchone()
        if row:
            self.id, self.message, self.urls, self.corres_url, self.corry_id = row
            return self
        else:
            return False

    def insert(self):
        self.curs.execute("insert into tweet (id, message, urls, corres_url, corry_id) values (?, ?, ?, ?, ?)",
                          (self.id, self.message, self.urls, self.corres_url, get_corry_id(self.corres_url)))
        self.db.conn.commit()
        return self

    @staticmethod
    def parse_json(data):
        urls = data['entities'].get('urls', None)
        corres_url = None
        if not urls:
            return False
        for url in urls:
            maybe_corry = url.get('expanded_url', None)
            if maybe_corry:
                if not 'thecorrespondent.com' in maybe_corry:
                    maybe_corry = Unshorten.unshorten(maybe_corry)
                    if 'thecorrespondent.com' in maybe_corry:
                        corres_url = maybe_corry
                        break
                else:
                    corres_url = maybe_corry
                    break

        if corres_url:
            cached = Tweet().get(data.get('id'))
            if not cached:
                print('.', sep='')
                return Tweet(id=data.get('id'), message=data.get('text'),
                      urls=json.dumps(urls), corres_url=corres_url).insert()
            return cached
        else:
            return False
