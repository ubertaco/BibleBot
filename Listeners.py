import re
import socket
import logging
import imaplib
from Bibles import parse_references
from TransactionObjects import Query, Response

logging.basicConfig(level=logging.DEBUG, filename='biblebot.log',
    format="[%(asctime)s %(module)s - %(name)s] {%(levelname)s} %(message)s")


class Listener:
    def __init__(self):
        pass

    def poll(self):
        raise NotImplementedError

    def get_new_queries(self):
        raise NotImplementedError


class ListenerFactory:
    @staticmethod
    def create_listener_from_config(conf):
        """Creates a listener from the specified configuration dictionary"""
        username = conf["username"]
        password = conf["password"]

        if conf["type"].lower() == "imap":
            del conf["type"]
            return IMAPListener(**conf)


class IMAPListener(Listener):
    def __init__(self, username, password, server='imap.gmail.com',
            port=993, label='inbox', use_ssl=True):
        """creates a new IMAPListener object, a wrapper for a IMAP account"""
        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.label = label
        self.use_ssl = use_ssl

    def connect(self):
        logging.info("Connecting to IMAP server %s on port %s" % (self.server,
            self.port))
        if self.use_ssl:
            self.connection = imaplib.IMAP4_SSL(self.server, self.port)
        else:
            self.connection = imaplib.IMAP4(self.server, self.port)
        logging.info("Logging into %s as %s" % (self.server, self.username))
        self.connection.login(self.username, self.password)
        logging.info("Successful login to IMAP!")
        self.connection.select(self.label)  # select label (inbox by default)

    def disconnect(self):
        logging.info("Logging %s out of %s" % (self.username, self.server))
        self.check_connection()
        self.connection.close()
        self.connection.logout()
        self.connection = None

    def poll(self):
        """Polls this IMAPListener's inbox for a count of new Queries."""
        return self.get_unread_count()

    def get_new_queries(self):
        """Fetches a list containing new Queries from this IMAPListener."""
        mails = self.get_unread_mails()
        queries = []
        for mail in mails:
            queries.append(IMAPListener.emailToQuery(mail))

        return queries

    def check_connection(self):
        """Returns True if connected, raises NoMailConnectionError if not."""
        if not self.connection:
            logging.error('No connection to inbox')
            raise NoMailConnectionError('No connection to inbox')
        else:
            return True

    def get_unread_count(self):
        """Gets the number of unread emails; returns an integer."""
        logging.info("Getting unread message count.")
        self.connect()
        if self.check_connection():
            self.refresh()
            rc, message = self.connection.status("inbox", "(UNSEEN)")
            unreadCount = re.search("UNSEEN (\d+)", str(message[0])).group(1)
            logging.info("Found %s unread messages." % unreadCount)
            self.disconnect()
            return int(unreadCount)

    def get_unread_mails(self):
        """Returns an iterable containing all unread messages as RFC822
        strings."""
        logging.info("Fetching new mail.")
        self.connect()
        if self.check_connection():
            self.refresh()
            logging.debug("Asking server for unread emails.")
            _, msg_ids = self.connection.uid("search", None, "(UNSEEN)")
            logging.debug("Server returned %s" % msg_ids)
            msg_ids = msg_ids[0].split()
            mails = []
            for msg_id in msg_ids:
                logging.debug("Fetching message with uid %s" % msg_id)
                _, data = self.connection.uid("fetch", msg_id, "(RFC822)")
                mails.append(data[0][1])

            self.disconnect()
            return mails

    def refresh(self):
        """Sends a noop to the IMAP inbox, refreshing our cached view of it."""
        logging.info("Refreshing inbox")
        self.connection.noop()

    @staticmethod
    def emailToQuery(msg_str):
        """Creates a new Query object from an RFC822-formatted string
        representing an email."""
        import email
        logging.info("Creating a new Query from incoming string: %s" % msg_str)
        msg = email.message_from_string(msg_str)
        debug_string = ""
        for k in msg.keys():
            debug_string += "\n%s = %s" % (str(k), str(msg[k]))
        logging.debug("email message object:%s" % debug_string)

        sender = msg['From']

        maintype = msg.get_content_maintype()
        body = ""
        if maintype == 'multipart':
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                    body = part.get_payload()

        elif maintype == 'text':
            body = msg.get_payload()

        logging.debug("Parsing references from email")
        passages = parse_references(body)

        return Query(passages=passages, sender=sender)
