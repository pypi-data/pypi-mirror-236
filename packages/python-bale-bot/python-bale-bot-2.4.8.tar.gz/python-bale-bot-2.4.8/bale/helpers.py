import re
from datetime import datetime

__all__ = (
    "create_deep_linked_url",
    "parse_time"
)

def create_deep_linked_url(bot_username: str, payload: str) -> str:
    """Creating a deep link for the bot.

    Parameters
    ----------
        bot_username: :class:`str`
            The username of bot.
        payload: :class:`str`
            The Payload of deep link
    """
    if len(bot_username) < 4 or not bot_username.lower().endswith('bot'):
        raise TypeError(
            "Please enter a Valid Username"
        )

    if not re.match(r"^[A-Za-z0-9_-]+$", payload):
        raise TypeError(
            "Please enter a Valid payload"
        )

    url = "ble.ir/{username}?start={payload}".format(username = bot_username, payload = payload)
    return url

def parse_time(data: int):
    return datetime.fromtimestamp(data)