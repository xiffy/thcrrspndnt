from mastodon import Mastodon

# Run this once
Mastodon.create_app(
    "dcrrspndntMasto",
    api_base_url="https://mastodon.nl",
    to_file="dcrrspndntMasto.secret",
)

mastodon = Mastodon(client_id="dcrrspndntMasto.secret")
access_token = mastodon.log_in("your-email", "your-password")

print(access_token)
