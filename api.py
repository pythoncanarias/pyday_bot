#!/usr/bin/env python

import requests
import logging

logger = logging.getLogger(__name__)


def args_as_url_params(data):
    return '&'.join([
        '{}={}'.format(k, data[k]) for k in data
    ])


class APIError(Exception):
    pass


class API:

    def __init__(self, base_url):
        self.base_url = base_url
        self.path = []

    def __getattr__(self, name):
        obj = API(self.base_url)
        obj.path = self.path.copy()
        obj.path.append(name)
        return obj

    def get_path(self, *args):
        steps = self.path.copy()
        if args:
            steps.extend(args)
        return '/'.join(steps)

    def get_url(self, *args):
        return '{}/{}'.format(
            self.base_url,
            self.get_path(*args),
            )

    def get_full_url(self, *args, **kwargs):
        return '{}{}'.format(
            self.get_url(*args),
            '?{}'.format(args_as_url_params(kwargs)) if kwargs else '',
        )

    def __call__(self, *args, **kwargs):
        logger.info('API calls {}'.format(self.get_full_url(*args, **kwargs)))
        url = self.get_url(*args)
        r = requests.get(url, params=kwargs)
        if r.status_code == 200:
            response = r.json()
            if response['status'] == 'ok':
                return response['result']
            else:
                raise APIError(response['message'])
        else:
            raise APIError('Error de protocolo HTTP: {}'.format(r.status_code))
