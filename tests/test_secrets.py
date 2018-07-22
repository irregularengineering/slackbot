# pylint: disable=missing-docstring,redefined-outer-name,wrong-import-order
"""
Tests for Secrets
"""

import os

import pytest

from slackbot.utils.secrets import Secrets, SecretNotFoundException


@pytest.fixture
def secrets():
    return Secrets('tests/resources/test_secrets')


def test_no_file():
    os.environ['test_wut'] = 'yep'
    secrets = Secrets('tests/the_wrong_file')
    assert secrets.get('test', 'wut') == 'yep'


def test_override(secrets):
    os.environ['SomeSecret_some_value'] = 'ponies'
    assert secrets.get('SomeSecret', 'some_value') == 'ponies'


def test_no_override(secrets):
    assert secrets.get('SomeSecret', 'something_else') == 'tacos'


def test_section_not_found(secrets):
    with pytest.raises(SecretNotFoundException):
        secrets.get('NotFound', 'not_ever')


def test_param_not_found(secrets):
    with pytest.raises(SecretNotFoundException):
        secrets.get('SomeOtherSecret', 'not_this_one')


def test_not_found_no_exception(secrets):
    assert secrets.get('Nope', 'not_here', raise_on_not_found=False) is None


def test_not_found_default(secrets):
    assert secrets.get('SomeOtherSecret', 'not_again', default='ni!') == 'ni!'
