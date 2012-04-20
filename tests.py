import unittest
import os
import re


def readConfigResourceFile(filename):
    with open(os.path.join("test", "resources", filename)) as infile:
        return infile.read()


class BibleTest(unittest.TestCase):
    """Tests correct functionality of the Bibles module."""

    def testParseReferences(self):
        """Test bible reference parsing"""
        from Bibles import parse_references
        expected_result = ["Rom. 12:2", """Romans
        12:2""", "Romans 12:2"]
        input_str = """test bar baz foo 123Rom. 12:2 bonkRomans 12:2 Romans
        12:2"""
        self.assertEquals(parse_references(input_str), expected_result)

    def testParseTranslations(self):
        """Test translation parsing"""
        from Bibles import parse_translations
        expected_result = ["ESV", "KJV"]
        input_str = """blar aohfwe ESV a;oihwef
        KJV"""
        self.assertEquals(parse_translations(input_str, expected_result))

    def testLookupPassage(self):
        """Test bible passage lookup in all translations"""
        import Bibles

        import json
        expected_result = json.loads(
                readConfigResourceFile("test_passages.json")
                )

        for translation in Bibles.translations.iterkeys():
            print("Testing %s lookup." % translation)
            result = Bibles.translations[translation].lookup("Romans 12:2")
            result = re.sub("\s+", " ", result)
            self.assertEquals(result, re.sub("\s+", " ",
                expected_result[translation]))


class SMTPSenderTest(unittest.TestCase):
    """Tests correct functionality of senders"""
    def testSMTPEncode(self):
        """Test encoding of Responses to text/plain MIME email for SMTP."""
        from Senders import SMTPSender
        from TransactionObjects import Response
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
        expected_result = Query(
                ['Rom. 12:2'], 'Spencer Williams <tapesmith@gmail.com>')
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


if __name__ == "__main__":
    unittest.main()
