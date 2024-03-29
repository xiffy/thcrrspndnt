import os

corres_version = os.getenv("CORRES_VERSION", "EN")

if corres_version == "EN":
    CONFIG = {
        "query": "thecorrespondent.com",
        "db": {"path": "data/db.sqlite3"},
        "twitter": {
            "account": "<your-tweet-bot-account>",
            "CONSUMER_KEY": "<it's keys>",
            "CONSUMER_SECRET": "<it's keys>",
            "OAUTH_KEY": "<it's keys>",
            "OAUTH_SECRET": "<it's keys>",
        },
        "twitter_post": {
            "SEND_TWEETS": False,
            "CONSUMER_KEY": "<it's keys>",
            "CONSUMER_SECRET": "<it's keys>",
            "OAUTH_KEY": "<it's keys>",
            "OAUTH_SECRET": "<it's keys>",
        },
    }
else:
    CONFIG = {
        "query": "decorrespondent.nl",
        "db": {"path": "data/db.NL.sqlite3"},
        "twitter": {
            "account": "<another twitter account (or the same)>",
            "CONSUMER_KEY": "<it's keys>",
            "CONSUMER_SECRET": "<it's keys>",
            "OAUTH_KEY": "<it's keys>",
            "OAUTH_SECRET": "<it's keys>",
        },
        "twitter_post": {
            "SEND_TWEETS": False,
            "CONSUMER_KEY": "<it's keys>",
            "CONSUMER_SECRET": "<it's keys>",
            "OAUTH_KEY": "<it's keys>",
            "OAUTH_SECRET": "<it's keys>",
        },
    }
