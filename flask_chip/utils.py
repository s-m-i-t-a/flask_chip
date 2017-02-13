# -*- coding: utf-8 -*-
import json

from flask import Response


def unauthorized():
    # type: () -> Response
    data = {
        'message': 'Unauthorized',
        'status': 401
    }
    return Response(
        json.dumps(data),
        data['status'],
        {'content-type': 'application/json'}
    )
