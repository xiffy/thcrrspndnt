import settings
from mastodon import Mastodon


class Tooter:
    def __init__(self):
        self.settings = settings.CONFIG["post"]
        self.instance = Mastodon(
            access_token=self.settings["access_token"],
            api_base_url=self.settings["api_base_url"],
        )

    def send_toot(self, article):
        send = self.settings.get("SEND_TOOTS", True)
        print(f"would send ==> {article.author}: {article.title} - {article.share_url}")
        if send:
            self.instance.status_post(
                f"{article.author}: {article.title} - {article.share_url}"
            )
