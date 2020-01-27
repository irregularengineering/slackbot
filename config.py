"""
Slackbot configuration
"""

import logging

from slackbot.utils.secrets import Secrets

secrets = Secrets()

BACKEND = 'Slack'
BOT_DATA_DIR = './data'
BOT_EXTRA_PLUGIN_DIR = './slackbot/plugins'
CORE_PLUGINS = ('ACLs', 'Help', 'Health', 'Utils')
BOT_LOG_FILE = BOT_DATA_DIR + '/err.log'
BOT_LOG_LEVEL = logging.INFO
BOT_ASYNC = True
BOT_ASYNC_POOLSIZE = 10
BOT_IDENTITY = {'token': secrets.get('Slackbot', 'token')}
BOT_ADMINS = ('@paul')
BOT_PREFIX = '!'
BOT_ALT_PREFIXES = ('@Bender', '@bender')
ACCESS_CONTROLS = {
    'restart': {'allowusers': BOT_ADMINS},
    'status': {'allowusers': BOT_ADMINS},
    'uptime': {'allowusers': BOT_ADMINS},
    'history': {'allowusers': BOT_ADMINS},
    'log tail': {'allowusers': BOT_ADMINS},
    'shutdown': {'allowusers': None},
    'status_gc': {'allowusers': None},
    'status_load': {'allowusers': None},
    'status_plugins': {'allowusers': None},
    'about': {'allowusers': None},
    'apropos': {'allowusers': None},
    'echo': {'allowusers': None},
    'render_test': {'allowusers': None},
}
HIDE_RESTRICTED_COMMANDS = True
HIDE_RESTRICTED_ACCESS = True
DIVERT_TO_PRIVATE = ('help', 'whoami', 'status', 'log tail')
