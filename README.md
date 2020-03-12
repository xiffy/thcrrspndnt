# :see_no_evil: :hear_no_evil: :speak_no_evil: thcrrspndnt 
thcrrspndnt is first of all a twitter-bot. It searches for a configurable `query` the twitter-api on behalf of your twitter account. (Did I mention you must have a twitter account and register an app to get this baby qorking?). Each found tweet is then parsed for the presence of a share url and unshortens any in between url shortners. 
If a valid URL is found in the tweet, the tweet get's stored. 
The URL is fetched (once) and vital information is collected with Beautiful Soup and stored in the database. If this is the first time the URL is seen, a tweet is (optionally) sent. 

This service is specifically designed for the Correspondent.nl/.com a Dutch / English site. 
You can see it in action here: https://molecule.nl/dcrrspndnt (dutch) and https://molecule.nl/thcrrspndnt theyare accompanied by [@dcrrspndnt](https://twitter.com/dcrrspndnt) and [@thcrsspndnton](https://twitter.com/thcrsspndnt) twitter respectively. 

#### I wants it
```git clone git@github.com:xiffy/thcrrspndnt.git
cd thcrrspndnt
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt
```

now edit settings.sample.py and fill in your twitter-secrets and your desired searchstring and save as settings.py

starting the bot, i've got the next lines inside my crontab
 
    */5 * * * *  cd /<hidden>project/thcrrspndnt/thcrrspndnt; /<hidden>/project/thcrrspndnt/venv/bin/python searcher.py >> /var/log/thcrrspndnt.log 2>&1
     export CORRES_VERSION=NL; cd /<hidden>/project/thcrrspndnt/thcrrspndnt; /<hidden>/project/thcrrspndnt/venv/bin/python searcher.py >> /var/log/dcrrspndnt.log 2>&1 

and this creates some logging for each site and crawls the web for each site.

When you invoke `start.sh` the english variant server will get started and will listen to port 5000,`startNL.sh` will start a server on port 5001. These are Flask servers and will offer a web interface to the cached articles. And you can access all articles for free :-)
 
 

:todo: tell how to obtain app-aproval
