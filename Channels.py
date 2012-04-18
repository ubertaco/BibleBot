from Listeners import *
from Senders import *
logging.basicConfig(level=logging.DEBUG, filename='biblebot.log',
    format="[%(asctime)s %(module)s - %(name)s] {%(levelname)s} %(message)s")

class Channel:
    def __init__(self, name, listener, sender):
        self.name = name
        self.listener = listener
        self.sender = sender

        import logging
        self.logger = logging.getLogger(self.name)

    def poll(self):
        self.logger.info("Polling listener")
        return self.listener.poll()

    def get_new_queries(self):
        self.logger.info("Fetching new queries")
        new_queries = self.listener.get_new_queries()
        for q in new_queries:
            q.channel = self
        return new_queries

    def send(self, response):
        self.logger.info("Sending %s" % response)
        self.sender.send(response)
