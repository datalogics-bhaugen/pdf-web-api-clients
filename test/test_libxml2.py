"libxml2 regression tests"

import libxml2
from nose.tools import assert_equal, assert_raises


XML = '<?xml version="1.0" encoding="UTF-8"?><status><authorized>true</authorized><plan>public</plan><usage_reports><usage_report metric="hits" period="minute"><period_start>2013-08-22 23:45:00 +0000</period_start><period_end>2013-08-22 23:46:00 +0000</period_end><max_value>10</max_value><current_value>0</current_value></usage_report></usage_reports></status>'


def test_exception():
    assert_raises(libxml2.parserError, libxml2.parseDoc, XML[:-1])

def test_get_content():
    root = libxml2.parseDoc(XML)
    assert_equal(root.xpathEval('/status/plan')[0].getContent(), 'public')

