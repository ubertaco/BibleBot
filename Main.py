#!/usr/bin/env python2
import time, json, os.path, logging, optparse
import Bibles, Conf, Channels
from TransactionObjects import Query, Response

logging.basicConfig(level=logging.DEBUG, filename='biblebot.log',
    format="[%(asctime)s %(module)s - %(name)s] {%(levelname)s} %(message)s")

parser = optparse.OptionParser(description="""BibleBot -- watches an email
    address for incoming scripture references, looks them up, and replies 
    back.""")
parser.add_option("-c", "--config", metavar="configpath", dest="configpath", 
    help="""Configuration file location""")
(opts, args) = parser.parse_args()

class BibleBot():
    def __init__(self, configpath=os.path.join(os.path.dirname(__file__),
    "BibleBot.conf")):
        self.channels = Conf.read_channels_from_configfile(configpath)
        logging.info("Loaded configuration from %s" % configpath)

    def run(self):
        while True:
            logging.info("Polling all channels")
            for channel in self.channels:
                new_queries = channel.poll()
                if new_queries > 0: # if there are new queries
                    logging.info("%d unread queries in channel %s!" %
                            (new_queries, channel.name))
                    logging.info("Fetching new queries from channel %s..." %
                            channel.name)
                    queries = channel.get_new_queries() # get unfulfilled queries 
                    logging.info("Got new queries.")
                    for query in queries: # for each query
                        for passage in query.passages: # for each scripture reference

                            # look up the passage
                            text = Bibles.translations["ESV"].lookup(passage)

                            # Create a reply with the body set to that passage
                            logging.info("Drafting a reply for %s to %s" %
                                    (passage, query.sender))
                            reply = Response(passage, text, query.sender)

                            # And send it
                            logging.info("Sending reply for %s to %s" % (passage,
                                query.sender))

                            channel.send(reply)

                logging.info("Sleeping for 15 seconds")
                time.sleep(15)

if opts.configpath: 
    biblebot = BibleBot(opts.configpath)
else:
    biblebot = BibleBot()
biblebot.run()
