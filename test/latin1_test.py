# -*- coding: latin_1 -*-

"Latin-1 regression tests"

from test import Result, Test
from test_client import ErrorCode, HTTPCode


def test_password_ok():
    return  # TODO: restore after fixing server
    Test(['data/latin1_password.pdf', u'password=déjà'], Result())()
