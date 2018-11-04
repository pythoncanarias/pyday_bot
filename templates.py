#!/usr/bin/env pythpn

from Cheetah.Template import Template


def render(template, **kwargs):
    with open(template, 'r') as f:
        tmpl = f.read()
    return str(Template(tmpl, searchList=[kwargs]))

