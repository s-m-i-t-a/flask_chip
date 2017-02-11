# -*- coding: utf-8 -*-

import pytest
import six
import time

if six.PY3:
    from unittest.mock import Mock, call, patch, sentinel
else:
    from mock import Mock, call, patch, sentinel

from pages.tests.factories import UserFactory
from auth import generate_token, verify_token


class SpecVerifyToken(object):

    @pytest.mark.usefixtures("db")
    def should_return_stored_data_when_token_is_right(self):
        user = UserFactory()
        token = generate_token(user)

        data = verify_token(token)

        assert data is not None
        assert data['id'] == str(user.id)

    @pytest.mark.usefixtures("db")
    def should_return_none_when_token_expire(self, app):
        user = UserFactory()
        token = generate_token(user, 0)

        time.sleep(1)

        data = verify_token(token)

        assert data is None

    @pytest.mark.usefixtures("db")
    def should_return_none_when_token_is_wrong(self, app):
        data = verify_token('')

        assert data is None
