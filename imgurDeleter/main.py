import sys

import praw
from config import config
from loguru import logger
from prawcore.exceptions import Forbidden

logger.remove(None)
logger.add(
    sys.stderr, format="<green>{time:HH:mm}" "</green> - <level>{message}</level>"
)
logger.add("./instance/last_run.log", rotation="50 MB", mode="w")


def search_and_destroy(r: praw.Reddit, subreddit: str, match: str):
    while True:
        query = list(
            r.subreddit(subreddit).search(f"url:{match}", sort="new", limit=None)
        )

        if (number := len(query)) == 0:
            logger.debug(f"No new submissions found matching {match!r}")
            return

        logger.debug(f"Found {number} in the first batch of urls matching {match!r}")

        for submission in query:
            logger.debug(f"Deleting post with url: {submission.url!r}")
            try:
                submission.mod.remove()
            except Forbidden:
                logger.critical("The bot account must be a moderator to remove posts!")
                sys.exit(1)


@logger.catch(onerror=lambda _: sys.exit(1))
def main() -> None:
    logger.debug(f"Running with config:\n{config!r}")

    r = praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent="u/thillsd imgur cleaner",
        username=config.username,
        password=config.password,
    )

    for url in config.removal_urls:
        search_and_destroy(r, subreddit=config.subreddit, match=url)


if __name__ == "__main__":
    main()
