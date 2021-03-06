'''
Created on Mar 8, 2019

@author: unicman
'''
import ConfigParser
import datetime
import imaplib
import os

def purgemails(server, port, login, password, folder="Zdelete", maxAge=30):
    # Deduct 1 from maxAge because imaplib does search excluding last date.
    before_date_friendly = (datetime.datetime.utcnow() - datetime.timedelta(maxAge)).strftime("%d-%b-%Y")
    before_date = before_date_friendly
    box = imaplib.IMAP4_SSL(server,port)
    box.login(login,password)
    box.select(folder)
    print "SUCCESS: Purging mails from {0}:{1} server {2} account and {3} folder".format(server, port, login, folder)
    typ, data = box.search(None, '(BEFORE {0})'.format(before_date))
    if data != ['']:
        count = data[0].split()[-1]
        print "SUCCESS: Found {0} mails before date {1}".format(count, before_date_friendly)
        box.store("1:{0}".format(count), '+FLAGS', '\\Deleted')
    else:
        print "SUCCESS: No expired messages found before date {0}.".format(before_date_friendly)

    print "SUCCESS: Expunging"
    box.expunge()
    box.close()
    box.logout()
    print "SUCCESS: Deleted mails before date {0}".format(before_date_friendly)

if __name__ == "__main__":
    configLocations = [ os.path.expanduser('~/purge-mails.cfg'), '/etc/purge-mails.cfg' ]

    config = None
    for confFile in configLocations:
        print "SUCCESS: Searching configuration in {0}".format(confFile)
        if os.path.isfile(confFile):
            config = ConfigParser.SafeConfigParser()
            config.readfp(open(confFile))
            break

    if config is None:
        print "ERROR: Configuration should be present in one of the folders."
        exit(1)

    for section in config.sections():
        server = config.get(section, 'server')
        port = config.getint(section, 'port')
        login = config.get(section, 'username')
        password = config.get(section, 'password')
        folder = config.get(section, 'folder')
        maxAge = config.getint(section, 'age')

        print "SUCCESS: Purging as per section {0}".format(section)
        purgemails(server, port, login, password, folder, maxAge) 

####
## Remove '#' at the beginning of each line.
## Copy-paste below content in home folder as file purge-mails.cfg
## You can have multiple sections with whatever name you like and
## each of those mailboxes will be purged.
####
#[section_1]
#server=imap.gmail.com
#port=993
#username=test@gmail.com
#password=foobar
#folder=folder1
#age=1
