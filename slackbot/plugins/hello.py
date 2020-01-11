# pylint: disable=no-self-use,too-many-ancestors
"""
Hello Plugin
"""

import re
import random

from errbot import BotPlugin, re_botcmd


RESPONSES = [
    'Good day!',
    'Hello!',
    'Yo!'
]


class Hello(BotPlugin):
    """
    Say hello, or whatever else we like
    """
    @re_botcmd(pattern=r'(hello|hey|yo|what\'s up)', re_cmd_name_help='hello', flags=re.IGNORECASE)
    def hello(self, _msg, _args):
        """
        Say hello
        """
        return random.choice(RESPONSES)
