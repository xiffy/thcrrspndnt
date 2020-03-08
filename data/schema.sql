CREATE TABLE unshorten (shorturl text, longurl text);
CREATE INDEX unshorten_shorturl on unshorten (shorturl);
CREATE TABLE article (corry_id text, share_url text UNIQUE, title text,
                      author text, created_at text, published_at text);
CREATE INDEX article_corry_id ON article (corry_id);
CREATE UNIQUE INDEX article_share_url ON article (share_url);
CREATE INDEX article_author on article (author);
CREATE TABLE tweet (id text, message text, urls text, corres_url text, corry_id text);
CREATE INDEX tweet_id on tweet (id);
CREATE INDEX tweet_corres_url on tweet (corres_url);
CREATE INDEX tweet_corry_id on tweet (corry_id);
