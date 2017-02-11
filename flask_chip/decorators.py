# -*- coding: utf-8 -*-
from functools import wraps

from flask import request, g
from flask_musers.models import User

from auth import unauthorized, verify_token as verify


def user_from_token(callback=None):
    '''
    Set put user to flask.g.

    callback -- None or function called when user or token not found

    If callback is None, then function set g.user to None.
    '''

    def verify_token(f):
        @wraps(f)
        def _verify_token(*args, **kwargs):
            data = verify(request.headers.get('X-Auth-Token', ''))
            if data is None:
                g.user = None
            else:
                g.user = User.get_active_user_by_pk_or_none(data['id'])

            if g.user is None and callback is not None:
                return callback()

            return f(*args, **kwargs)
        return _verify_token

    return verify_token


verify_token = user_from_token(unauthorized)
logged_user = user_from_token()
