# -*- coding: utf-8 -*-

"server regression tests"

import platform

import mock
import test
from test import Result, Test
from test_client import ErrorCode, HTTPCode
from nose.tools import assert_in


def test_bad_url():
    errors = (HTTPCode.BadRequest, HTTPCode.UnsupportedMediaType)
    result = Result(ErrorCode.InvalidInput, errors)
    try: Test(['http://127.0.0.1/spam.pdf'], result)()
    except Exception as exception:
        assert_in(max_retry_error('/spam.pdf'), str(exception))

def max_retry_error(url):
    return 'Max retries exceeded with url: {}'.format(url)

def test_good_url():
    Test(['http://www.datalogics.com/pdf/doc/pdf2img.pdf'], Result())()

def test_bad_pdf():
    result = Result(ErrorCode.InvalidInput, HTTPCode.UnsupportedMediaType)
    Test(['data/bad.pdf'], result)()

def test_truncated_pdf():
    result = Result(ErrorCode.InvalidInput, HTTPCode.BadRequest)
    Test(['data/truncated.pdf'], result)()

def test_ascii_password_ok():
    password = 'password=Kraftfahrzeughaftpflichtversicherung'
    Test(['data/user_password.pdf', password], Result())()

def test_utf8_password_ok():
    return  # TODO: add server support for UTF-8 strings
    Test(['data/two_passwords.pdf', u'password=紙容量紙容量'], Result())()

def test_windows_1252_password_ok():
    return  # TODO: add server support for Windows-1252 strings
    Test(['data/windows_1252_password.pdf', 'password=déjà'], Result())()

def test_missing_owner_password():
    result = Result(ErrorCode.MissingPassword, HTTPCode.Forbidden)
    Test(['data/owner_password.pdf'], result)()

def test_invalid_owner_password():
    result = Result(ErrorCode.InvalidPassword, HTTPCode.Forbidden)
    Test(['data/owner_password.pdf', 'password=spam'], result)()

def test_missing_user_password():
    result = Result(ErrorCode.MissingPassword, HTTPCode.Forbidden)
    Test(['data/user_password.pdf'], result)()

def test_invalid_user_password():
    result = Result(ErrorCode.InvalidPassword, HTTPCode.Forbidden)
    Test(['data/user_password.pdf', 'password=spam'], result)()

def test_user_password_instead_of_owner():
    result = Result(ErrorCode.InvalidPassword, HTTPCode.Forbidden)
    return  # TODO: add server support for UTF-8 strings
    Test(['data/two_passwords.pdf', u'password=紙容量'], result)()

def test_adept_drm():
    result = Result(ErrorCode.UnsupportedSecurityProtocol, HTTPCode.Forbidden)
    Test(['data/ADEPT-DRM.pdf'], result)()

def test_live_cycle():
    pass  # TODO: need test data

def test_pki_certificate():
    result = Result(ErrorCode.UnsupportedSecurityProtocol, HTTPCode.Forbidden)
    Test(['data/PKI_certificate.pdf'], result)()

def test_insufficient_memory(): _memory_error('scripts/insufficient_memory')
def test_out_of_memory(): _memory_error('scripts/out_of_memory')

def _memory_error(mock_script):
    request_entity_too_large = HTTPCode.RequestEntityTooLarge
    result = Result(ErrorCode.RequestTooLarge, request_entity_too_large)
    with mock.Client(mock_script):
        Test(['data/bad.pdf'], result)()

def test_pdf2img_crash():
    result = Result(ErrorCode.UnknownError, HTTPCode.InternalServerError)
    with mock.Client('../bin/segfault'):
        Test(['data/bad.pdf'], result)()
