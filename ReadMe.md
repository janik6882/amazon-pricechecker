# Requirements:
The following python modules will be required: <br />
* requests
* BeautifulSoup 4
* json

# Getting started:
You will need two files, one called "creds.json" and one calles "input.json".<br />
Scheme for "input.json":<br />
```
{
  "url": "Amazon URL to watch",
  "price": Desired price as int,
  "last": 0
}
```

Scheme for "creds.json": <br />
```
{
  "telegram_bot": "Telegram Bot api token",
  "notify_true": "User ID for user to notify about changes/desired price reached",
  "notify_false": "User ID for user to notify when nothing changed"
}
```
