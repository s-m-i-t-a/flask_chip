# -*- coding: utf-8 -*-

import pytest
import six

if six.PY3:
    from unittest.mock import Mock, call, patch, sentinel
else:
    from mock import Mock, call, patch, sentinel

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from pages.tests.factories import UserFactory
from auth import generate_token


class SpecGenerateToken(object):

    @pytest.mark.usefixtures("db")
    def should_generated_token_is_string(self):
        user = UserFactory()
        token = generate_token(user)

        assert isinstance(token, six.string_types)

    @pytest.mark.usefixtures("db")
    def should_generated_token_contains_usrer_id(self, app):
        user = UserFactory()
        token = generate_token(user)

        s = Serializer(app.config['SECRET_KEY'])
        data = s.loads(token)

        assert data['id'] == str(user.id)
