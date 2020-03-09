import logging
import jinja2
from flask import Flask, Response, request, render_template, session, redirect
from model.article import Article

# setup basic config for the given log level
#logging.basicConfig(level=('DEBUG' if config.DEBUG else config.LOG_LEVEL))

def home():
    articles = Article().get_paged()
    payload = render_template('home.html', articles=articles)
    return payload

def author(name):
    articles = Article().get_author_paged(name)
    payload = render_template('author.html', articles=articles, static_depth='..', author=name)
    return payload

def rss():
    articles = Article().get_paged()
    payload = render_template('rss.xml', articles=articles)
    return Response(payload, mimetype='text/xml')

def create_thcrrspndnt():
    app = Flask('thcrrspndnt')
    app.add_url_rule('/', view_func=home)
    app.add_url_rule('/author/<name>', view_func=author)
    app.add_url_rule('/rss', view_func=rss)
    return app

app = create_thcrrspndnt()