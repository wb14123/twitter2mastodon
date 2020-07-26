
# Twitter2Mastodon

This project can export Twitter posts to Mastodon. There are
already some projects doing that. But this one will also change the post
time for the imported post. Need to be able to access Mastodon's
database in order to do that.

## Usage

### 1. Clone this project.

### 2. Install dependencies:

```
pip install -r requirements.txt
```

### 3. Change the config

Change the fields in `config.py`.

### 4. Register Mastodon App and Login

Run this command: 

```
python register_mastodon.py
```

This will register a Mastodon app called `twitter_importer` and
login the user.

### 5. Export Twitter posts to Mastodon

```
mkdir tmp
python main.py
```

This will import all the posts from Twitter to Mastodon. The media
attached in the posts will be downloaded to `tmp/` and uploaded to
Mastodon later.

This command may stuck and fail because of rate limit for Mastodon
API. It will output the Twitter ID it's processing. So if you want
to restart the porgram, change `twitter_max_id` in `config.py` to
import from that tweet.

It will download all the tweets from the user first and store them
in the memory. The reason is we want to reverse the timeline and
import from the earliest one. So if you have a lot of tweets and
a small memory, it may not be able to import.



