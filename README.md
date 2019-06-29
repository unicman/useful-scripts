# useful-scripts

## ssh-add-keys.sh

Simple script that looks for SSH private keys and adds them using ssh-add command. It assumes that ssh-agent is already running. And another good part is if putty-tools package is installed, it detects Putty Private keys, converts them to openssh format and then execute ssh-add!

*Usage:* 
```
bash ssh-add-keys.sh <timeout> <dir>
```
*Legend:*
  `timeout` - optional. default infinite. how long key should be retained by SSH agent. E.g. 1h, 1d, 1w, 1m etc. 
  `dir` - optional. default ~/.ssh/key.d/. directory where all SSH private keys are stored.

## purge-mails.py

Fetches all the mails present in certain IMAP folder and based on specified age, deletes + expunges all older mails to free up IMAP box space.

*Pre-requisite:* Create purge-mails.cfg with contents.
```
[CONFIG1]
server=<imap-server-host>
port=<imap-server-port>
username=<username>
password=<password>
folder=<IMAP-folder-full-path>
age=<mails-to-keep-in-days>
  
...
```
For manual execution, store at ~/purge-mails.cfg. For configuring cron job, store at /etc/purge-mails.cfg. Change permission to 600 to avoid credentials leaking out.

*Manual Usage:*
```
python purge-mails.py
```

*Cron Usage:* To configure daily clean-up activity, create cron job under /etc/cron.daily/purge-mails.cron

```
#!/bin/sh

PURGE_OUTPUT=/tmp/purge-mails-$(date -u "+%Y-%m-%dT%H%M").txt

/usr/bin/python /scratch/mbhandek/github/useful-scripts/python/purge-mails.py > $PURGE_OUTPUT 2>&1
```

Change permission to 700 to start daily cron job. 
