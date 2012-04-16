import unittest
import re

# TODO: unit tests for SMTPSender, IMAPListener, and all TransactionObjects  

class BibleTest(unittest.TestCase):
    """Tests correct functionality of the Bibles module."""

    def testParseReferences(self):
        """ Test reference parsing (should return a tuple of bible verse
        references parsed from an input string"""
        from Bibles import parse_references
        print("Testing reference parsing")
        expected_result = ["Rom. 12:2", """Romans
        12:2""", "Romans 12:2"]
        input_str = """test bar baz foo 123Rom. 12:2 bonkRomans 12:2 Romans
        12:2"""
        self.assertEquals(parse_references(input_str), expected_result)

    def testLookupPassage(self):
        import Bibles
        """Test bible lookup """

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

class SenderTest(unittest.TestCase):
    """Tests correct functionality of senders"""
    def testSMTPSend(self):
        import TransactionObjects, smtpd
        # debugServer = smtpd.DebuggingServer("127.0.0.1")


class ListenerTest(unittest.TestCase):
   """Tests correct functionality of Listeners."""

   def test
