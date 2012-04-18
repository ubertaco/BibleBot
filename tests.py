import unittest
import os, re

def readConfigResourceFile(filename):
    with open(os.path.join("test", "resources", filename)) as infile:
        return infile.read()

class BibleTest(unittest.TestCase):
    """Tests correct functionality of the Bibles module."""

    def testParseReferences(self):
        """Test bible reference parsing"""
        from Bibles import parse_references
        print("Testing reference parsing")
        expected_result = ["Rom. 12:2", """Romans
        12:2""", "Romans 12:2"]
        input_str = """test bar baz foo 123Rom. 12:2 bonkRomans 12:2 Romans
        12:2"""
        self.assertEquals(parse_references(input_str), expected_result)

    def testLookupPassage(self):
        """Test bible passage lookup in all translations"""
        import Bibles

        expected_result = {}
        expected_result["ESV"] = re.sub("\s+", " ", u"""Romans 12:2
      [2]Do not be conformed to this world, but be transformed by the
    renewal of your mind, that by testing you may discern what is the will of
    God, what is good and acceptable and perfect. (ESV)""")

        for translation in Bibles.translations.iterkeys():
            print("Testing %s lookup." % translation)

            result = Bibles.translations[translation].lookup("Romans 12:2")
            result = re.sub("\s+", " ", result)
            self.assertEquals(result, expected_result[translation])

            result = Bibles.translations[translation].lookup("Rom. 12:2")
            result = re.sub("\s+", " ", result)
            self.assertEquals(result, expected_result[translation])

if __name__ == "__main__":
    unittest.main()

class SMTPSenderTest(unittest.TestCase):
    """Tests correct functionality of senders"""
    def testSMTPEncode(self):
        """Test encoding of Responses to text/plain MIME email for SMTP."""
        from Senders import SMTPSender
        from TransactionObjects import Response
        import TransactionObjects, subprocess, sys
        msg = Response(passage="Rom. 12:2", text="test test test",
        recipient="foo@foo.com")
        expected_result = """Content-Type: text/plain; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
From: BibleBot <biblebot@ninjatricks.net>
To: foo@foo.com
Subject: Rom. 12:2

test test test"""
        self.assertEquals(SMTPSender.encode(msg), expected_result)

class ListenerTest(unittest.TestCase):
   """Tests correct functionality of Listeners."""

   def testEmailToQuery(self):
       """Test conversion of RFC822 email strings to Queries"""
       from Listeners import IMAPListener
       from TransactionObjects import Query
       testmail = readConfigResourceFile("test_rec_mail")
       expected_result = Query(['Rom. 12:2'], 'Spencer Williams <tapesmith@gmail.com>')
       result = IMAPListener.emailToQuery(testmail)
       self.assertEquals(result.passages, expected_result.passages)
       self.assertEquals(result.sender, expected_result.sender)

class ConfigTest(unittest.TestCase):
    """Tests correct config parsing."""

    def testChannelsFromConfig(self):
        """Test creation of channels from a config file"""
        import Conf 
        from Channels import Channel
        from Listeners import Listener
        from Senders import Sender
        testconfig = readConfigResourceFile("test_configuration.conf")
        channels = Conf.read_channels_from_config(testconfig)
        for c in channels:
            self.assertIsInstance(c, Channel)
            self.assertIsInstance(c.listener, Listener)
            self.assertIsInstance(c.sender, Sender)
            self.assertEquals(c.name, "test_channel")
