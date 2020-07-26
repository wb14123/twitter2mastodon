class Config:
    twitter_consumer_key = ""
    twitter_consumer_secret = ""
    twitter_access_token = ""
    twitter_access_token_secret = ""
    twitter_user_screen_name = ""

    # If set, the tweets with id larger than this will not be imported. Useful if the importing is failed and
    # want to import again from the failed point
    twitter_max_id = None

    mastodon_url = ""

    # The mastodon username that you want to import
    mastodon_username = ""

    # The mastodon user's password
    mastodon_password = ""

    # The file to store app's sec file. The directory must be exists.
    mastodon_app_sec_file = ""

    # The file to store user's sec file. The directory must be exists.
    mastodon_user_sec_file = ""

    # The postgres information for mastodon
    db_database = ""
    db_user = "postgres"
    db_password = ""
    db_host = "127.0.0.1"
    db_port = "5432"


config = Config()
