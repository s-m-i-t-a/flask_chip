# -*- coding: utf-8 -*-
import json

from flask import Response, current_app as app

from itsdangerous import SignatureExpired, BadSignature, TimedJSONWebSignatureSerializer as Serializer


def generate_token(user, expiration=24*60*60):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': str(user.id)})
    return token.decode('ascii')


def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return None

    return data


def unauthorized():
    data = {
        'message': 'Unauthorized',
        'status': 401
    }
    return Response(
        json.dumps(data),
        data['status'],
        {'content-type': 'application/json'}
    )
