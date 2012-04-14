from Listeners import *
from Senders import *
logging.basicConfig(level=logging.DEBUG, filename='biblebot.log',
format="[%(asctime)s %(module)s] {%(levelname)s} %(message)s")

class Channel:
    def __init__(self, name, listener, sender)
        self.name = name
        self.listener = listener
        self.sender = sender

        import logging
        logger = logging.Logger(self.name)

    def poll(self):
        logger.info("Polling listener")
        return self.listener.poll()

    def get_new_queries(self):
        logger.info("Fetching new queries")
        return self.listener.get_new_queries()

    def send(self, response):
        logger.info("Sending %s" % response)
        self.sender.send(response)

