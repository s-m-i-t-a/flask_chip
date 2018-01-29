# -*- coding: utf-8 -*-
'''
Generate token and verify
'''

from datetime import datetime
from itsdangerous import (
    SignatureExpired,
    BadSignature,
    JSONWebSignatureSerializer as Serializer
)
from pyresult import ok, error, rmap, and_then
from toolz import pipe


EPOCH = datetime(1970, 1, 1)


def generate(data, key, **kwargs):
    ''' Generate JWT token with supplied data

    >>> from flask_chip.tokens import generate

    >>> key = "y):'QGE8M-b+MEKl@k4e<;*9.BqL=@~B"
    >>> data = {'foo': 1234}
    >>> generate(data, key, iat=1516788472)
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
eyJkYXRhIjp7ImZvbyI6MTIzNH0sImlhdCI6MTUxNjc4ODQ3MiwiZXhwIjoxNTE2ODc0ODcyfQ.\
TPuT1svUpzXa5GlU3HtuSZm6-Dy9vlX3HOxpM53iyrY'
    '''
    iat = kwargs.get('iat', _now())
    exp = kwargs.get('exp', 24 * 60 * 60)

    claim = {
        'data': data,
        'iat': iat,
        'exp': _expires_in(iat, exp),
    }

    serializer = Serializer(key)
    token = serializer.dumps(claim, header_fields={'typ': 'JWT'})
    return token.decode('utf-8')


def verify(token, key):
    ''' Check the supplied token and it's expiration.

    :param token: A token to verify
    :param key: decryption key
    :returns: result with data

    ## Examples

    returns data if token is valid

    >>> from flask_chip.tokens import generate

    >>> key = "y):'QGE8M-b+MEKl@k4e<;*9.BqL=@~B"
    >>> data = {'foo': 1234}
    >>> token = generate(data, key=key)
    >>> verify(token, key=key)
    Result(status='Ok', value={'foo': 1234})

    returns expiration error when token expire

    >>> from time import sleep

    >>> key = "y):'QGE8M-b+MEKl@k4e<;*9.BqL=@~B"
    >>> data = {'foo': 1234}
    >>> token = generate(data, key=key, exp=0)
    >>> sleep(1)  # wait for token expiration
    >>> verify(token, key=key)
    Result(status='Error', value='Token expired.')

    returns time travele error

    >>> from datetime import datetime

    >>> iat = round(datetime.timestamp(datetime.utcnow())) + 3600
    >>> key = "y):'QGE8M-b+MEKl@k4e<;*9.BqL=@~B"
    >>> data = {'foo': 1234}
    >>> token = generate(data, key=key, iat=iat)
    >>> verify(token, key=key)
    Result(status='Error', value='Token traveled through time.')

    returns error if token is invalid

    >>> key = "y):'QGE8M-b+MEKl@k4e<;*9.BqL=@~B"
    >>> data = {"foo": 1234}
    >>> token = generate(data, key=key)
    >>> key2 = "12345678901234567890123456789012"
    >>> verify(token, key=key2)
    Result(status='Error', value='invalid JWT')
    '''
    serializer = Serializer(key)
    try:
        return pipe(
            token,
            serializer.loads,
            ok,
            and_then(_expired),  # pylint: disable=no-value-for-parameter
            and_then(_time_traveled),  # pylint: disable=no-value-for-parameter
            rmap(lambda d: d['data'])  # pylint: disable=no-value-for-parameter
        )
    except (SignatureExpired, BadSignature, TypeError):
        return error('invalid JWT')


def _expires_in(issued_at, expires_in):
    return issued_at + expires_in


def _now():
    return round(datetime.timestamp(datetime.utcnow()))


def _expired(data):
    return ok(data) if data['exp'] >= _now() else error('Token expired.')


def _time_traveled(data):
    return ok(data) if data['iat'] <= _now() else error('Token traveled through time.')
