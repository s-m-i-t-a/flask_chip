# -*- coding: utf-8 -*-

import json

from mock import call, patch
from six.moves import http_client as http

from auth import unauthorized


class SpecUnauthorizedResponse(object):

    @patch('auth.Response')
    def should_return_response(self, mock_response):
        result = unauthorized()

        assert mock_response.called
        assert result == mock_response.return_value

    @patch('auth.Response')
    def should_call_response_with_401_and_message_as_json(self, mock_response):
        data = {
            'message': 'Unauthorized',
            'status': http.UNAUTHORIZED
        }
        msg = json.dumps(data)

        unauthorized()

        assert mock_response.call_args == call(msg, data['status'], {'content-type': 'application/json'})
