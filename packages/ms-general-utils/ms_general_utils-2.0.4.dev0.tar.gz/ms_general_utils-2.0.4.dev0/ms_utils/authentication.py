import json

import requests
from flask import g, current_app, request

from ms_utils import abort_bad_request


class NotAuthenticate(object):
    def dispatch_request(self, **kwargs):
        user = None
        try:
            response = requests.get(f'{current_app.config.get("AUTH_MS_API")}/auth/check-authentication',
                                    headers=request.headers)
            if response.status_code == 200:
                response = json.loads(response.content)
                user = response['data']
        except Exception:
            pass
        g.setdefault('user', user)
        return super(NotAuthenticate, self).dispatch_request(**kwargs)


class IsAuthenticate(object):
    def dispatch_request(self, **kwargs):
        config = current_app.config
        if 'AUTH_MS_API' in config.keys():
            raise ReferenceError("The authentication API (AUTH_MS_API) is not configured")

        response = requests.get(f'{current_app.config.get("AUTH_MS_API")}/auth/check-authentication',
                                headers=request.headers)
        if not response.status_code == 200:
            abort_bad_request()
        response = json.loads(response.content)
        g.setdefault('user', response['data'])
        return super(IsAuthenticate, self).dispatch_request(**kwargs)
