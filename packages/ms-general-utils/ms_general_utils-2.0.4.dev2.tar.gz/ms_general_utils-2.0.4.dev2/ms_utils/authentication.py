import json

from flask import g, current_app

from ms_utils import abort_bad_request, abort_unauthorized, request_get


class NotAuthenticate(object):
    def dispatch_request(self, **kwargs):
        user = None
        try:
            response = request_get(f'{current_app.config.get("AUTH_MS_API")}/auth/check-authentication')
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
        if not config.get('AUTH_MS_API'):
            abort_bad_request('The authentication API (AUTH_MS_API) is not configured')

        response = request_get(f'{current_app.config.get("AUTH_MS_API")}/auth/check-authentication')
        if not response.status_code == 200:
            abort_unauthorized()
        response = json.loads(response.content)
        g.setdefault('user', response['data'])
        return super(IsAuthenticate, self).dispatch_request(**kwargs)
