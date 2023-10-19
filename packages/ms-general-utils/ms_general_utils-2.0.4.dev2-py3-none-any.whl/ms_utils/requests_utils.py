import requests
from flask import request


def request_get(url, params=None, headers=None):
    if headers is None:
        headers = {}
    if params is None:
        params = {}
    return requests.get(url, params=params, headers={**headers, **request.headers})


def request_post(url, data=None, headers=None):
    if headers is None:
        headers = {}
    if data is None:
        data = {}
    return requests.post(url, json=data, headers={**headers, **request.headers})
