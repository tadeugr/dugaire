import requests


def get(url):
    """Request URL and return the result."""

    res = requests.get(url)
    return res.text
