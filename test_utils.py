#!/usr/bin/env python

import pytest
import utils


def test_one():
    assert utils.as_integer('one') == (True, 1)


def test_uno():
    assert utils.as_integer('uno') == (True, 1)


def test_string_1():
    assert utils.as_integer('1') == (True, 1)


def test_dos():
    assert utils.as_integer('dos') == (True, 2)


def test_tres():
    assert utils.as_integer('tres') == (True, 3)


def test_doce():
    assert utils.as_integer('doce') == (True, 12)


def test_none():
    assert utils.as_integer(None) == (False, None)


def test_float_exact():
    assert utils.as_integer(1.0) == (True, 1)


def test_float_not_exact():
    assert utils.as_integer(1.5) == (False, 1.5)


if __name__ == '__main__':
    pytest.main()
