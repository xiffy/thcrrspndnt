import logging
import jinja2
import os
from flask import Flask, Response, request, render_template, session, redirect
from model.article import Article
from model.tweet import Tweet

# setup basic config for the given log level
#logging.basicConfig(level=('DEBUG' if config.DEBUG else config.LOG_LEVEL))

def home():
    start, amount = pager_args()
    articles = Article().get_paged(start=start, amount=amount)
    tot_count = Article().get_count_filtered()
    tweet_count = Tweet().get_tweetcount_filtered()
    payload = render_template('home.html', articles=articles, start=int(start), amount=int(amount),
                              tot_count=tot_count, tweet_count=tweet_count,
                              cssver=os.path.getmtime('thcrrspndnt/static/thcrrspndnt.css')[:10])
    return payload

def rss():
    articles = Article().get_paged(start=0, amount=100)
    payload = render_template('rss.xml', articles=articles)
    return Response(payload, mimetype='text/xml')

def author(name):
    start, amount = pager_args()
    articles = Article().get_author_paged(name, start=start, amount=amount)
    tot_count = Article().get_count_filtered(author=name)
    tweet_count = Tweet().get_tweetcount_filtered(author=name)
    payload = render_template('author.html', articles=articles, static_depth='../..', author=name,
                              start=int(start), amount=int(amount), tot_count=tot_count, tweet_count=tweet_count,
                              cssver=os.path.getmtime('thcrrspndnt/static/thcrrspndnt.css'[:10]))
    return payload

def rss_author(name):
    articles = Article().get_author_paged(name, start=0, amount=100)
    payload = render_template('rss.xml', articles=articles)
    return Response(payload, mimetype='text/xml')

def pager_args():
    start = request.args.get('start', 0)
    amount = request.args.get('amount', 20)
    return (start, amount)

def create_thcrrspndnt():
    app = Flask('thcrrspndnt')
    app.add_url_rule('/', view_func=home)
    app.add_url_rule('/rss', view_func=rss)
    app.add_url_rule('/author/<name>/', view_func=author)
    app.add_url_rule('/author/<name>/rss', view_func=rss_author)
    return app

app = create_thcrrspndnt()