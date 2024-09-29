import os

from collections import namedtuple
from tapo import ApiClient


ApiCredentials = namedtuple("ApiCredentials", ["username", "password", "address"])


def load_credentials():
    credentials = ApiCredentials(
        os.getenv("TAPO_USERNAME"),
        os.getenv("TAPO_PASSWORD"),
        os.getenv("TAPO_ADDRESS"),
    )

    if not credentials.username or not credentials.password or not credentials.address:
        raise ValueError("TAPO_USERNAME, TAPO_PASSWORD, and TAPO_ADDRESS must be set")

    return credentials

def new_client():
    credentials = load_credentials()

    timeout_seconds = 1
    return ApiClient(credentials.username, credentials.password, timeout_seconds)
