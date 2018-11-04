#!/usr/bin/env python

from unittest.mock import Mock
import pytest
import event
import json


@pytest.fixture(scope="module")
def evt():
    api = Mock()
    api.events = Mock()
    with open('test_event_sample.json', 'r') as f:
        api.events.return_value = json.load(f)
    return event.Event('test', api=api)


def test_event_name(evt):
    assert evt.name == 'PyDay Tenerife 2018' 


def test_event_desc(evt):
    assert evt.desc == "El evento anual de Python más "  \
                       "importante que se celebra en Tenerife"


def test_event_tracks(evt):
    assert len(evt.tracks) == 3
    assert evt.tracks[0].name == 'Tatooine'
    assert evt.tracks[1].name == 'Hoth'
    assert evt.tracks[2].name == 'Dagobah'


def test_event_talks(evt):
    first_track = evt.tracks[0]
    assert len(first_track.talks) == 6
    talk = first_track.talks[0]
    assert talk.name == "Desarrolla tu primer módulo en ansible"
    assert talk.start == "11:00"
    assert talk.end == "11:50"
    assert talk.description.startswith('Ansible es una navaja suiza')
    assert talk.description.endswith('mostraremos como empezar.')
    assert talk.tags == ['devops-tools', ]
    assert talk.language == "ES"


if __name__ == '__main__':
    pytest.main()


