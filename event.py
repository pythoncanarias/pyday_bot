#!/usr/bin/env python

import logging
from prettyconf import config
from collections import defaultdict
from api import API

logger = logging.getLogger(__name__)


api = API(config('PYTHON_CANARIAS_API'))


class Talk:

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', '')
        self.start = kwargs.pop('start', '')
        self.end = kwargs.pop('end', '')
        self.description = kwargs.pop('description', '')
        self.tags = kwargs.pop('tags', [])
        self.language = kwargs.pop('language', 'es')


class Track:
    def __init__(self, **kwargs):
        self.track_id = kwargs.pop('track_id', None)
        self.order = kwargs.pop('order', 0)
        self.name = kwargs.pop('name', '')
        self.talks = [
            Talk(**t) for t in kwargs.pop('talks', [])
            ]
        for t in self.talks:
            t.track = self


class Event:

    def __init__(self, tagname, api=api):
        self.tagname = tagname
        self.load_from_api(api)

    def load_from_api(self, api):
        data = api.events(self.tagname)
        self.name = data['name']
        self.desc = data['short_description']
        self.url = data['url']
        self.tracks = [
            Track(**_) for _ in data['tracks']
            ]
        self.num_tracks = len(self.tracks)
        self.tags = defaultdict(list)
        for talk in self.all_talks():
            for tag in talk.tags:
                self.tags[tag].append(talk)

    def all_talks(self):
        for track in self.tracks:
            for talk in track.talks:
                yield(talk)

    def is_valid_track(self, num):
        return 0 < num <= self.num_tracks
