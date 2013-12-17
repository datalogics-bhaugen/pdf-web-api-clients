# -*- coding: utf-8 -*-

"UTF-8 regression tests"

from test import Result, Test
from test_client import ErrorCode, HTTPCode


# TODO: add UTF-8 support to server on Linux (ignore failures until then)

def test_password_ok():
    Test(['data/two_passwords.pdf', u'password=紙容量紙容量'], Result())()

def test_missing_owner_password():
    result = Result(ErrorCode.MissingPassword, HTTPCode.Forbidden)
    Test(['data/two_passwords.pdf'], result)()

def test_invalid_owner_password():
    result = Result(ErrorCode.InvalidPassword, HTTPCode.Forbidden)
    Test(['data/two_passwords.pdf', 'password=spam'], result)()

def test_user_password_instead_of_owner():
    result = Result(ErrorCode.InvalidPassword, HTTPCode.Forbidden)
    Test(['data/two_passwords.pdf', u'password=紙容量'], result)()
