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
                return Tweet(id=data.get('id'), message=data.get('text'),
                      urls=json.dumps(urls), corres_url=corres_url).insert()
            return cached
        else:
            return False


"""
      'created_at': 'Sat Mar 07 19:49:03 +0000 2020',
      'id': 1236378347917185026,
      'id_str': '1236378347917185026',
      'text': 'Truth be sold: how truth became a product - \u2066@robwijnberg\u2069\nThe Correspondent https://t.co/Dqtb5AUkXH',
      'truncated': False,
      'entities': {
        'hashtags': [],
        'symbols': [],
        'user_mentions': [
          {
            'screen_name': 'robwijnberg',
            'name': 'Rob Wijnberg',
            'id': 118026200,
            'id_str': '118026200',
            'indices': [
              45,
              57
            ]
          }
        ],
        'urls': [
          {
            'url': 'https://t.co/Dqtb5AUkXH',
            'expanded_url': 'https://thecorrespondent.com/322/truth-be-sold-how-truth-became-a-product/7514229030-36b9d1cf',
            'display_url': 'thecorrespondent.com/322/truth-be-s…',
            'indices': [
              77,
              100
            ]
          }
        ]
      },
      'metadata': {
        'iso_language_code': 'en',
        'result_type': 'recent'
      },
      'source': '<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>',
      'in_reply_to_status_id': None,
      'in_reply_to_status_id_str': None,
      'in_reply_to_user_id': None,
      'in_reply_to_user_id_str': None,
      'in_reply_to_screen_name': None,
      'user': {
        'id': 306126928,
        'id_str': '306126928',
        'name': 'Ellen Timmer',
        'screen_name': 'Ellen_Timmer',
        'location': 'Nederland',
        'description': 'Advocaat / attorney-at-law (@pellicaan). Weblog: https://t.co/5IbjrmWEhB Motto: goede bedoelingen rechtvaardigen geen slechte regels',
        'url': 'https://t.co/WLvf1gozXr',
        'entities': {
          'url': {
            'urls': [
              {
                'url': 'https://t.co/WLvf1gozXr',
                'expanded_url': 'https://ellentimmer.com',
                'display_url': 'ellentimmer.com',
                'indices': [
                  0,
                  23
                ]
              }
            ]
          },
          'description': {
            'urls': [
              {
                'url': 'https://t.co/5IbjrmWEhB',
                'expanded_url': 'https://ellentimmer.com/',
                'display_url': 'ellentimmer.com',
                'indices': [
                  49,
                  72
                ]
              }
            ]
          }
        },
        'protected': False,
        'followers_count': 1153,
        'friends_count': 534,
        'listed_count': 134,
        'created_at': 'Fri May 27 10:12:04 +0000 2011',
        'favourites_count': 1457,
        'utc_offset': None,
        'time_zone': None,
        'geo_enabled': False,
        'verified': False,
        'statuses_count': 58307,
        'lang': None,
        'contributors_enabled': False,
        'is_translator': False,
        'is_translation_enabled': False,
        'profile_background_color': 'C0DEED',
        'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png',
        'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png',
        'profile_background_tile': True,
        'profile_image_url': 'http://pbs.twimg.com/profile_images/1158711540062785538/4pbtztO__normal.jpg',
        'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1158711540062785538/4pbtztO__normal.jpg',
        'profile_banner_url': 'https://pbs.twimg.com/profile_banners/306126928/1403861403',
        'profile_link_color': '0084B4',
        'profile_sidebar_border_color': 'C0DEED',
        'profile_sidebar_fill_color': 'DDEEF6',
        'profile_text_color': '333333',
        'profile_use_background_image': True,
        'has_extended_profile': False,
        'default_profile': False,
        'default_profile_image': False,
        'following': False,
        'follow_request_sent': False,
        'notifications': False,
        'translator_type': 'none'
      },
      'geo': None,
      'coordinates': None,
      'place': None,
      'contributors': None,
      'is_quote_status': False,
      'retweet_count': 0,
      'favorite_count': 0,
      'favorited': False,
      'retweeted': False,
      'possibly_sensitive': False,
      'lang': 'en'
    },
"""