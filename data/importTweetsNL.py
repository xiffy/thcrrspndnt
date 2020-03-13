from thcrrspndnt.model.article import Article, get_corry_id
from thcrrspndnt.model.tweet import Tweet
import settings
import csv
import decimal

# make sure we use the right database
settings.CONFIG['db'] = {'path': 'data/db.NL.sqlite3',}
ctx = decimal.Context()
# 20 digits should be enough for everyone :D
ctx.prec = 20

def float_to_str(f):
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')

with open('/c/Users/averschoor/pythonprojects/thcrrspndnt/tweetdump.data') as records:
    csv_reader = csv.reader(records, delimiter='\t')
    ids = []
    doublures = []
    broken = []
    count = 0
    char_count = 0
    for row in csv_reader:
        count += 1
        if count % 1000 == 0:
            print('.', end='')
            char_count += 1
            if char_count % 100 == 0:
                print('')
        old_id = row[0]
        corry_id = get_corry_id(row[1])
        article = Article().get(corry_id=corry_id)
        if not article:
            broken.append(corry_id)
            print('^', end='')
            char_count += 1
            if char_count % 100 == 0:
                print('')
            continue
        tweet_id = float_to_str(float(old_id.replace(',', '.')))
        share_url = article.share_url

        ids.append(tweet_id)
        new_tweet = Tweet(id=tweet_id, message='imported tweet', corry_id=corry_id, corres_url=share_url)
        new_tweet.insert()

    print('Geen artikel gevonden: %s' % len(broken))
    print('Tot imported %s' % len(ids))
