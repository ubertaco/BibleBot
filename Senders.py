import logging, smtplib
from TransactionObjects import Response
from Mail import NoMailConnectionError
logging.basicConfig(level=logging.DEBUG, filename='biblebot.log',
    format="[%(asctime)s %(module)s - %(name)s] {%(levelname)s} %(message)s")

class Sender:
    def __init__(self):
        pass

    def send(self, msg):
        raise NotImplementedError
        pass

class SenderFactory:
    @staticmethod
    def create_sender_from_config(conf):
        """Creates a sender from the specified configuration dictionary"""
        if conf["type"].lower() == "smtp":
            logging.info("Creating new SMTP Sender")
            del conf["type"]
            return SMTPSender(**conf) 

class SMTPSender(Sender):
    def __init__(self, username, password, server='smtp.gmail.com',
            port=587, use_ssl=True):
        """Creates a new SMTPSender object"""
        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.use_ssl = use_ssl

    def connect(self):
        # Initiate connection
        logging.info("Connecting to SMTP server %s on port %s as %s" % (self.server,
            self.port, self.username))
        connection = smtplib.SMTP(self.server, self.port)
        connection.ehlo()
        if self.use_ssl:
            connection.starttls()
            connection.ehlo()
        connection.login(self.username, self.password)

        # if successful, that's our SMTP connection for this sender
        self.connection = connection
        logging.info("Successful login to SMTP!")

    def check_connection(self):
        """Returns True if connected, raises NoMailConnectionError if not."""
        if not self.connection:
            logging.error('No connection to mail sender')
            raise NoMailConnectionError('No connection to mail sender')
        else:
            return True
    
    def send(self, response):
        """Sends a response object using the current SMTP connection"""
        logging.info("Sending response:\r\n %s" % str(response))
        self.connect()
        if self.check_connection:
            self.connection.sendmail("BibleBot <biblebot@ninjatricks.net>",
                    response.recipient, SMTPSender.encode(response))

    @staticmethod
    def encode(msg):
        """Encodes a Response object as a 'text/plain' email for SMTP"""
        from email.mime.text import MIMEText
        logging.info("Encoding message.")

        encodedMsg = MIMEText(msg.text)
        encodedMsg['From'] = "BibleBot <biblebot@ninjatricks.net>"
        encodedMsg['To'] = msg.recipient
        encodedMsg['Subject'] = "%s" % msg.passage
        logging.info("Encoded message: %s" % encodedMsg.as_string())
        return encodedMsg.as_string()
