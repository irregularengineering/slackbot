# Slackbot

## Prerequisites

You will need to set up acounts on Twitter and IEX and create API keys for each.  You will also need to set up a bot on Slack and grab its token.

Then set up a local file in ~/.secrets containing the secrets as shown.

```
[IEX]
token=notyourtoken

[Slackbot]
token=notyourtoken

[Twitter]
api_key=notyourkey
api_secret=notyoursecret
oauth_token=notyourtoken
oauth_secret=notyoursecret
```

## Run

```bash
./launch -b
```

## Test

```bash
py.test
```

## Lint

```bash
pylint slackbot tests
```
