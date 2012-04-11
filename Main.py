#!/usr/bin/env python2
import time, json, os.path, logging, argparse
import Mail, Bibles

logging.basicConfig(level=logging.DEBUG, filename='biblebot.log',
format="[%(asctime)s %(module)s] %(message)s")

parser = argparse.ArgumentParser(description="""BibleBot -- watches an email
    address for incoming scripture references, looks them up, and replies 
    back.""")
parser.add_argument("-c", "--config", metavar="configpath", dest="configpath", 
    help="""Configuration file location""")
args = parser.parse_args()

class BibleBot():
    def __init__(self, configpath=os.path.join(os.path.dirname(__file__),
    "BibleBot.conf")):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/biblebot.pid'
        self.pidfile_timeout = 5
        if os.path.exists(configpath) and os.path.isfile(configpath):
            with open(configpath, 'r') as configfile:
                config = configfile.read().strip()
                if config:
                    self.configuration = json.loads(config)
                else:
                    self.create_default_config(configpath)
            logging.info("Loaded configuration from %s" % configpath)
        else:
            self.create_default_config(configpath)

        logging.info("Opening imap connection")
        self.inbox = Mail.Inbox(username=self.configuration['imap_username'],
                password=self.configuration['imap_password'],
                imap_server=self.configuration['imap_hostname'],
                imap_port=self.configuration['imap_port'],
                label=self.configuration['imap_label'])


    def create_default_config(self, configpath):
        logging.info("""No configuration found at specified or default
                    location, creating new config there.""")
        self.configuration = json.loads("""
        {
            "imap_hostname" : "imap.example.com",
            "imap_port"     : 993,
            "imap_username" : "foo@example.com",
            "imap_password" : "password",
            "imap_label"    : "inbox",
            "smtp_username" : "foo@example.com",
            "smtp_password" : "password",
            "smtp_hostname" : "smtp.example.com",
            "smtp_port"     : 587,
            "smtp_use_ssl"  : True,
            "check_interval": 15,
        }""")

        logging.info("Config file saved to %s" % configpath)
        with open(configpath, "w") as configfile:
            json.dump(self.configuration, configfile, indent=4)

    def run(self):
        while True:
            logging.info("Polling for new mail")
            unread_count = self.inbox.get_unread_count()
            if unread_count > 0: # if there is unread mail
                logging.info("%d unread messages found!" % unread_count)
                logging.info("Fetching these messages...")
                mails = self.inbox.get_unread_mails() # get unread messages
                logging.info("Got unread messages.")
                for mail in mails: # for each message
                    # parse out scripture references
                    reference_list = Bibles.parse_references(mail.body) 
                    logging.info("Found requests for: %s" % 
                            ','.join(reference_list))

                    for reference in reference_list: # for each scripture reference
                        # look up the passage
                        passage = Bibles.translations["ESV"].lookup(reference)
                        # Create a reply with the body set to that passage
                        logging.info("Drafting a reply for %s to %s" %
                                (reference, mail.sender[1]))
                        reply = mail.create_reply(passage)
                        # And send it
                        logging.info("Sending reply for %s to %s" % (reference,
                            mail.sender[1]))

                        logging.debug("Opening SMTP connection")
                        sender = Mail.Sender(username=self.configuration['smtp_username'],
                                password=self.configuration['smtp_password'],
                                smtp_server=self.configuration['smtp_hostname'],
                                smtp_port=self.configuration['smtp_port'],
                                use_ssl=self.configuration['smtp_use_ssl'])
                        logging.debug("Sending mail")
                        sender.send_message(reply)

            logging.info("Sleeping for %d seconds" % self.configuration['check_interval'])
            time.sleep(self.configuration['check_interval'])
            self.inbox.refresh() # refresh inbox

if args.configpath: 
    biblebot = BibleBot(args.configpath)
else:
    biblebot = BibleBot()
biblebot.run()
