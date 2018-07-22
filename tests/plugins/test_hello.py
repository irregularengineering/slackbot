# pylint: disable=invalid-name,missing-docstring,import-error
"""
Test Hello plugin
"""

from slackbot.plugins import hello

pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = '.'


def test_hello(testbot):
    testbot.push_message('!hello')
    assert testbot.pop_message() in hello.RESPONSES
    testbot.push_message('!hey')
    assert testbot.pop_message() in hello.RESPONSES
    testbot.push_message("!what's up?")
    assert testbot.pop_message() in hello.RESPONSES
    testbot.push_message('!yo wutup')
    assert testbot.pop_message() in hello.RESPONSES
