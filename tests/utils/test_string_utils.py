# pylint: disable=missing-docstring
"""
Tests for String Utils
"""

from slackbot.utils import string_utils


def test_string_utils():
    assert string_utils.pluralize(-1) == 's'
    assert string_utils.pluralize(0) == 's'
    assert string_utils.pluralize(1) == ''
    assert string_utils.pluralize(2) == 's'
