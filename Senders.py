import logging
from TransactionObjects import Response
from Mail import NoMailConnectionError

class Sender:
    def __init__(self):
        pass

    def send(self, msg):
        raise NotImplementedError

class SMTPSender(Sender):
    def __init__(self, username, password, smtp_server='smtp.gmail.com',
            smtp_port=587, use_ssl=True):
        import smtplib
        import email

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
        logging.info("Sending response:\r\n %s" % str(response))

        self.connection.sendmail("BibleBot <biblebot@ninjatricks.net>",
                msg.recipient, encode(response))

    @staticmethod
    def encode(msg):
        """Encodes a Response object as a 'text/plain' email for SMTP"""
        from email.mime.text import MIMEText
        logging.info("Encoding message.")

        encodedMsg = MIMEText(msg.text)
        msg['From'] = "BibleBot <biblebot@ninjatricks.net>"
        msg['To'] = msg.recipient
        msg['Subject'] = "%s" % msg.passage
        logging.info("Encoded message: %s" % msg.as_string())
        return msg.as_string()
