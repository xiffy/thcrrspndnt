import logging
import jinja2
from flask import Flask,request, render_template, session, redirect
from model.article import Article

# setup basic config for the given log level
#logging.basicConfig(level=('DEBUG' if config.DEBUG else config.LOG_LEVEL))

def home():
    all = Article().get_paged()
    print(all)
    payload = render_template('home.html', articles=all)
    return payload


def create_thcrrspndnt():
    app = Flask('thcrrspndnt')
    app.add_url_rule('/', view_func=home)
    return app

app = create_thcrrspndnt()