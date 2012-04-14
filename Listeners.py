import re, socket
import logging
from Bibles import parse_references
from TransactionObjects import Query, Response


class Listener:
    def __init__(self):
        pass

    def poll(self):
        raise NotImplementedError

    def get_new_queries(self):
        raise NotImplementedError


class IMAPListener(Listener):
    """username, password, imap_server='imap.gmail.com', imap_port=993
    creates a new Inbox object, a wrapper for a IMAP account"""
    def __init__(self, username, password, imap_server='imap.gmail.com',
        import email
            imap_port=993, label='inbox'):
        """Creates a new Mailbox object, connected to the supplied IMAP server with the
        supplied username+password, and points it at the inbox for that account"""
        import imaplib # import necessary libs
        logging.info("Connecting to IMAP server %s on port %s as %s" % (imap_server,
            imap_port, username))
        self.connection = imaplib.IMAP4_SSL(imap_server, imap_port)
        self.connection.login(username, password)
        logging.info("Successful login to IMAP!")
        self.connection.select(label) # select label (inbox by default)

    def poll(self):
        self.refresh()
        return self.get_unread_count()

    def get_new_queries(self):
        mails = self.get_unread_mails()
        queries = []
        for mail in mails:
             queries.append(Query(mail.body.parse_references(), mail.sender))

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
        if self.check_connection():
            rc, message = self.connection.status("inbox", "(UNSEEN)")
            unreadCount = re.search("UNSEEN (\d+)", str(message[0])).group(1)
            logging.info("Found %s unread messages." % unreadCount)
            return int(unreadCount)

    def get_unread_mails(self):
        """Returns an iterable containing all unread messages."""
        logging.info("Fetching new mail.")
        if self.check_connection():
            logging.debug("Asking server for unread emails.")
            _, msg_ids = self.connection.uid("search", None, "(UNSEEN)")
            logging.debug("Server returned %s" % msg_ids)
            msg_ids = msg_ids[0].split()
            mails = []
            for msg_id in msg_ids:
                logging.debug("Fetching message with uid %s" % msg_id)
                _, data = self.connection.uid("fetch", msg_id, "(RFC822)")
                msg = Message.from_string(data[0][1])
                mails.append(msg)

            return mails

    def refresh(self):
        logging.info("Refreshing inbox")
        self.connection.noop()

class SMTPSender:
    def __init__(self, username, password, smtp_server='smtp.gmail.com',
            smtp_port=587, use_ssl=True):
        import smtplib

        # Initiate connection
        logging.info("Connecting to SMTP server %s on port %s as %s" % (smtp_server,
            smtp_port, username))
        self.connection = smtplib.SMTP(smtp_server, smtp_port)
        self.connection.ehlo()
        if use_ssl:
            self.connection.starttls()
            self.connection.ehlo()
        self.connection.login(username, password)

        logging.info("Successful login to SMTP!")

    def check_connection(self):
        """Returns True if connected, raises NoMailConnectionError if not."""
        if not self.connection:
            logging.error('No connection to mail sender')
            raise NoMailConnectionError('No connection to mail sender')
        else:
            return True
    
    def send(self, reponse):
        """Sends a response object using the current SMTP connection"""
        logging.info("Sending response:\r\n %s" % str(msg))

        self.connection.sendmail("BibleBot <biblebot@ninjatricks.net>", msg.recipient, msg.encode())

    @staticmethod
    def encode(msg):
        """Encodes the message for SMTP sending"""
        from email.mime.text import MIMEText
        logging.info("Encoding message.")
        encodedMsg = MIMEText(self.body)
        msg['From'] = "BibleBot <biblebot@ninjatricks.net>"
        msg['To'] = msg.recipient
        msg['Subject'] = "%s" % msg.passage
        return msg.as_string()

class Message:
    def __init__(self, body=None, sender=None, subject=None,
        recipients=None):
        self.body = body
        self.sender = sender
        self.subject = subject
        self.recipients = recipients

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.encode()

    @staticmethod
    def from_string(msg_str):
        """Creates a new Message object from an RFC822-formatted string
        representing an email."""
        logging.info("Creating a new message from incoming string: %s" %
                msg_str)
        msg = email.message_from_string(msg_str)
        debug_string = ""
        for k in msg.keys():
            debug_string += "\n%s = %s" % (str(k), str(msg[k]))
        logging.debug("email message object:%s" % debug_string)
        result = Message()

        if msg['Subject']:
            result.subject = msg['Subject'] 
        else:
            result.subject = "No subject"

        result.recipients = []
        if msg['To']:
            if type(msg['To']) is str:
                result.recipients.append(email.utils.parseaddr(msg['To']))
            else:
                for recipient in msg['To']:
                    result.recipients.append(email.utils.parseaddr(recipient))

        result.sender = email.utils.parseaddr(msg['From'])

        maintype = msg.get_content_maintype()
        if maintype == 'multipart':
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                   result.body = part.get_payload()
            
        elif maintype == 'text':
            result.body = msg.get_payload()

        return result

    def create_reply(self, body="No text"):
        """Creates a new Message object representing a reply to the current
        Message"""
        logging.info("Creating reply.")
        reply = Message()
        reply.recipients = [self.sender]
        reply.sender = email.utils.formataddr(("BibleBot",
            "bible@ninjatricks.net"))
        reply.body = body
        reply.subject = "RE:%s" % self.subject
        return reply


class NoMailConnectionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
