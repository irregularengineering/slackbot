# -*- coding: utf-8 -*-
from errbot import BotPlugin
from errbot import botcmd
from itertools import chain
import requests
import logging
import json
import re
import os
import random

from slackbot.utils.secrets import Secrets

secrets = Secrets()

log = logging.getLogger(name='errbot.plugins.Jira')

CONFIG_TEMPLATE = {'API_URL': secrets.get('Jira', 'JIRA_URL'),
                   'USERNAME': secrets.get('Jira', 'JIRA_USERNAME'),
                   'PASSWORD': secrets.get('Jira', 'JIRA_PASSWORD'),
                   'OAUTH_ACCESS_TOKEN': None,
                   'OAUTH_ACCESS_TOKEN_SECRET': None,
                   'OAUTH_CONSUMER_KEY': None,
                   'OAUTH_KEY_CERT_FILE': None,
                   'FIELD_CHECK': "customfield_901103"}

try:
    from jira import JIRA, JIRAError
except ImportError:
    log.error("Please install 'jira' python package")


class Jira(BotPlugin):
    """An errbot plugin for working with Atlassian JIRA"""

    def configure(self, configuration):
        if configuration is not None and configuration != {}:
            config = dict(chain(CONFIG_TEMPLATE.items(),
                                configuration.items()))
        else:
            config = CONFIG_TEMPLATE
        super(Jira, self).configure(config)

    def check_configuration(self, configuration):
        # TODO(alex) do some validation here!
        pass

    def get_configuration_template(self):
        """Returns a template of the configuration this plugin supports"""
        return CONFIG_TEMPLATE

    def activate(self):
        if self.config is None:
            # Do not activate the plugin until it is configured
            message = 'Jira not configured.'
            self.log.info(message)
            self.warn_admins(message)
            return

        self.jira_connect = self._login()
        if self.jira_connect:
            super().activate()

    def _login_oauth(self):
        """"""
        api_url = self.config['API_URL']
        # TODO(alex) make this check more robust
        if self.config['OAUTH_ACCESS_TOKEN'] is None:
            message = 'oauth configuration not set'
            self.log.info(message)
            return False

        key_cert_data = None
        cert_file = self.config['OAUTH_KEY_CERT_FILE']
        try:
            with open(cert_file, 'r') as key_cert_file:
                key_cert_data = key_cert_file.read()
            oauth_dict = {
                'access_token': self.config['OAUTH_ACCESS_TOKEN'],
                'access_token_secret': self.config['OAUTH_ACCESS_TOKEN_SECRET'],
                'consumer_key': self.config['OAUTH_CONSUMER_KEY'],
                'key_cert': key_cert_data
            }
            authed_jira = JIRA(server=api_url, oauth=oauth_dict)
            self.log.info('logging into {} via oauth'.format(api_url))
            return authed_jira
        except JIRAError:
            message = 'Unable to login to {} via oauth'.format(api_url)
            self.log.error(message)
            return False
        except TypeError:
            message = 'Unable to read key file {}'.format(cert_file)
            self.log.error(message)
            return False

    def _login_basic(self):
        """"""
        api_url = self.config['API_URL']
        username = self.config['USERNAME']
        password = self.config['PASSWORD']

        try:
            authed_jira = JIRA(server=api_url, basic_auth=(username, password))
            self.log.info('logging into {} via basic auth'.format(api_url))
            return authed_jira
        except Exception as e:
            message = 'Unable to login to {} via basic auth'.format(api_url)
            self.log.error(message, e)
            return False

    def _login(self):
        """"""
        self.jira_connect = None
        self.jira_connect = self._login_oauth()
        if self.jira_connect:
            return self.jira_connect
        self.jira_connect = None
        self.jira_connect = self._login_basic()
        if self.jira_connect:
            return self.jira_connect
        return None

    def _verify_valid_issue_id(self, msg, issue):
        issue = issue.lower()
        if issue == '':
            self.send(msg.frm,
                      'issue id cannot be empty',
                      message_type=msg.type,
                      in_reply_to=msg,
                      groupchat_nick_reply=True)
            return ''
        matches = []
        regexes = []
        regexes.append(r'([^\W\d_]+)\-(\d+)')  # e.g.: issue-1234
        regexes.append(r'([^\W\d_]+)(\d+)')    # e.g.: issue1234
        for regex in regexes:
            matches.extend(re.findall(regex, msg.body, flags=re.I | re.U))
        if matches:
            for match in set(matches):
                return match[0].upper() + '-' + match[1]
        self.send(msg.frm,
                  'issue id format incorrect',
                  message_type=msg.type,
                  in_reply_to=msg,
                  groupchat_nick_reply=True)
        return ''

    # TODO: refactor
    def _verify_is_jira(self, msg):
        matches = []
        regexes = []
        regexes.append(r'([^\W\d_]+)\-(\d+)')  # e.g.: issue-1234
        regexes.append(r'([^\W\d_]+)(\d+)')    # e.g.: issue1234
        for regex in regexes:
            matches.extend(re.findall(regex, msg.body, flags=re.I | re.U))
        if matches:
            for match in set(matches):
                return match[0].upper() + '-' + match[1]
        return None


    def get_data(self, json_object, search, name, key):
        for dict in json_object:
            if dict[search] == name:
                return dict[key]

    @botcmd(split_args_with=' ')
    def jira(self, msg, args):
        """Returns the subject of the issue and a link to it.
            !jira test-123"""
        issue = self._verify_valid_issue_id(msg, args.pop(0))
        if issue is '':
            return
        jira = self.jira_connect
        try:
            issue = jira.issue(issue)

            response = '({4}) "{0}" (by {2})\nassigned to {1} - {3}'.format(
                issue.fields.summary,
                issue.fields.assignee,
                issue.fields.reporter,
                issue.permalink(),
                issue.fields.status.name
            )

        except JIRAError:
            response = 'issue {0} not found.'.format(issue)
        self.send(msg.frm,
                  response,
                  groupchat_nick_reply=True)

    @botcmd(split_args_with=' ')
    def jira_create(self, msg, args):
        """Creates a new issue"""
        """not implemented yet"""

        jira = self.jira_connect
        try:
            issue_dict = {
                    'project': "SHAN",
                    'summary': 'New issue from jira-python',
                    'description': 'Look into this one',
                    'issuetype': {'name': 'Task'},
                    }

            new_issue = jira.create_issue(fields=issue_dict)

            response = '({4}) "{0}" (by {2})\nassigned to {1} - {3}'.format(
                new_issue.fields.summary,
                new_issue.fields.assignee,
                new_issue.fields.reporter,
                new_issue.permalink(),
                new_issue.fields.status.name
            )

        except JIRAError as e:
            response = 'we have error: {0}'.format(e)
            return

        self.send(msg.frm,
                  response,
                  groupchat_nick_reply=True)

        return "will create an issue"

    @botcmd(split_args_with=' ')
    def jira_assign(self, msg, args):
        """(Re)assigns an issue to a given user
            !jira assign infra-1033 pk"""

    # issue.update(assignee={'name': 'new_user'})
        return "not implemented"

    def callback_message(self, msg):
        """A callback which responds to mention of JIRA issues"""
        if not self.config:
            return

        # TODO: refactor
        if self._verify_is_jira(msg):
            issue = self._verify_is_jira(msg)
            if issue is '':
                return
            jira = self.jira_connect
            try:
                issue = jira.issue(issue)

                response = '({4}) "{0}" (by {2})\nassigned to {1} - {3}'.format(
                    issue.fields.summary,
                    issue.fields.assignee,
                    issue.fields.reporter,
                    issue.permalink(),
                    issue.fields.status.name
                )

            except JIRAError:
                response = 'issue {0} not found.'.format(issue)

            self.send_card(body=response,
                  to=msg.frm,
                  in_reply_to=msg,
                  title=issue.fields.summary,
            )

        if re.findall(r"(\d+)",msg.body):
            lottery_ticket = random.randint(1,1000)

            if lottery_ticket >= 998:
                response = "<3 @pk"
                self.send_card(body=response,
                  to=msg.frm,
                  in_reply_to=msg,
                  title="That's a Numberwang",
                  image="https://vignette.wikia.nocookie.net/thatmitchellandwebb/images/1/13/Numberwang.jpg"
                )