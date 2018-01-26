# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,redefined-outer-name,invalid-name

import time
import pytest  # type: ignore
import six

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask_chip.tokens import generate, verify


@pytest.fixture
def key():
    return 'secretkey'


@pytest.fixture
def data():
    return {'foo': ['bar', 'baz']}


@pytest.fixture
def token(data, key):
    return generate(data, key)


@pytest.fixture
def expired_token(data, key):
    return generate(data, key, 0)


def test_generated_token_is_string(key):
    data = {'foo': ['bar', 'baz']}
    token = generate(data, key)

    assert isinstance(token, six.string_types)


def test_generated_token_contains_usrer_id(key):
    data = {'foo': ['bar', 'baz']}
    token = generate(data, key)

    s = Serializer(key)
    result = s.loads(token)

    assert result == data


def test_return_stored_data_when_token_is_right(data, key, token):
    result = verify(token, key)

    assert result is not None
    assert result == data


def test_return_none_when_token_expire(key, expired_token):
    time.sleep(1)

    result = verify(expired_token, key)

    assert result is None


def test_return_none_when_token_is_wrong(key):
    result = verify('', key)

    assert result is None
