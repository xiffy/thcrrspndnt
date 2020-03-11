from thcrrspndnt.model.article import Article
import settings
import csv

# make sure we use the right database
settings.CONFIG['db'] = {'path': 'data/db.NL.sqlite3',}

with open('/tmp/artdump.txt') as records:
    csv_reader = csv.reader(records, delimiter=',')
    for row in csv_reader:
        corry_id = row[0]
        share_url = row[1]
        title = row[2]
        author = row[3]
        published_at = row[4]
        description = row[5]

        if not Article().get(corry_id=corry_id):
            new_article = Article(corry_id=corry_id, share_url=share_url, title=title, author=author, created_at=None,
                                  published_at=published_at, description=description)
            new_article.insert()
            print('.', end='')
        else:
            print('Already here ', corry_id)

