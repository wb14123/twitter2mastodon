from mastodon import Mastodon
from config import config

# Only need to create app once
Mastodon.create_app(
    'twitter_importer',
    api_base_url=config.mastodon_url,
    to_file=config.mastodon_app_sec_file
)

mastodon = Mastodon(
    client_id=config.mastodon_app_sec_file,
    api_base_url=config.mastodon_url
)

mastodon.log_in(
    config.mastodon_username,
    config.mastodon_password,
    to_file=config.mastodon_user_sec_file
)
