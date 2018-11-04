#!/usr/bin/env python

import pytest
from api import API


def test_create():
    api = API('http://pythoncanarias.es/api/v1')
    assert api.base_url == 'http://pythoncanarias.es/api/v1'
    assert len(api.path) == 0


def test_create_and_compose():
    api = API('http://pythoncanarias.es/api/v1')
    assert isinstance(api, API)
    assert isinstance(api.status, API)
    assert len(api.status.path) == 1
    assert api.status.path == ['status']
    assert api.status.get_url() == 'http://pythoncanarias.es/api/v1/status'


def test_single_call():
    api = API('http://pythoncanarias.es/api/v1')
    assert api.status.get_url() == 'http://pythoncanarias.es/api/v1/status'


def test_call_status():
    api = API('http://pythoncanarias.es/api/v1')
    status = api.status()
    assert status['active']
    assert status['version'] >= 1


if __name__ == '__main__':
    pytest.main()
