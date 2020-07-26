import tweepy
import psycopg2
import base64
from mastodon import Mastodon
import urllib.request
from config import config


class TwitterReader:
    def __init__(self, name, max_id=None, since_id=None):
        consumer_key = config.twitter_consumer_key
        consumer_secret = config.twitter_consumer_secret
        access_token = config.twitter_access_token
        access_token_secret = config.twitter_access_token_secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        self.name = name
        self.count = 20
        self.max_id = max_id
        self.since_id = since_id

    def read(self):
        tweets = self.api.user_timeline(
            screen_name=self.name, count=self.count, max_id=self.max_id, tweet_mode="extended",
            include_ext_media_availability=True, include_ext_alt_text=True)
        if self.max_id is not None:
            tweets = tweets[1:]
        if len(tweets) == 0:
            return []
        if self.since_id is not None and tweets[0].id < self.since_id:
            return []
        results = []
        for tweet in tweets:
            if (not tweet.is_quote_status) and (tweet.in_reply_to_screen_name is None or
                                                tweet.in_reply_to_screen_name == self.name):
                # print(tweet.created_at)
                for url in tweet.entities['urls']:
                    tweet.full_text = tweet.full_text.replace(url['url'], url['expanded_url'])
                if tweet.entities.get('media') is not None:
                    tweet.entities['pics'] = []
                    for m in tweet.extended_entities['media']:
                        tweet.full_text = tweet.full_text.replace(m['url'], "")
                        tweet.entities['pics'].append(m['media_url_https'])
                # print(tweet.id)
                # print(tweet.full_text)
                results.append(tweet)
        self.max_id = tweets[-1].id
        return results

    def read_all(self):
        results = []
        tweets = None
        while tweets is None or len(tweets) > 0:
            tweets = self.read()
            results += tweets
            print("Read %d tweets" % len(results))
            print("max_id: " + str(self.max_id))
        return results


class MastodonWriter:
    def __init__(self, since_id=None):
        self.mastodon = Mastodon(
            access_token=config.mastodon_user_sec_file,
            api_base_url=config.mastodon_url)
        self.db_conn = psycopg2.connect(
            database=config.db_database,
            user=config.db_user,
            password=config.db_password,
            host=config.db_host,
            port=config.db_port)
        self.db_cursor = self.db_conn.cursor()
        self.since_id = since_id

    def write(self, tweet):
        if self.since_id is not None and tweet.id < self.since_id:
            return
        print("Writing tweet ID: " + tweet.id_str)
        if tweet.entities.get('pics') is not None:
            media_ids = self.upload_pics(tweet.entities['pics'])
            toot = self.mastodon.status_post(tweet.full_text, media_ids=media_ids)
        else:
            toot = self.mastodon.toot(tweet.full_text)
        self.db_cursor.execute("update statuses set created_at = %s, updated_at = %s where id=%s",
                               (tweet.created_at, tweet.created_at, toot.id))
        self.db_conn.commit()
        print("Wrote tweet ID: %s, tote ID: %d" % (tweet.id_str, toot.id))

    def upload_pics(self, urls):
        ids = []
        for url in urls:
            file = self.get_url_file(url)
            print("Downloading pic, url: " + url)
            urllib.request.urlretrieve(url, file)
            print("uploading media, file: " + file)
            media_id = self.mastodon.media_post(file)['id']
            ids.append(media_id)
        return ids

    @staticmethod
    def get_url_file(url):
        return 'tmp/' + base64.encodebytes(str.encode(url)).decode('utf-8').strip()


reader = TwitterReader(config.twitter_user_screen_name, None, config.twitter_max_id)
writer = MastodonWriter(config.twitter_max_id)
all_tweets = reader.read_all()
for t in reversed(all_tweets):
    writer.write(t)
