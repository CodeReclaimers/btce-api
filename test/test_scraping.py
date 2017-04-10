from datetime import datetime
import sys
import unittest

import btceapi


class TestScraping(unittest.TestCase):
    def test_scrape_main_page(self):
        mainPage = btceapi.scrapeMainPage()
        for message in mainPage.messages:
            msgId, user, time, text = message
            assert type(time) is datetime
            if sys.version_info[0] == 2:
                # python2.x
                assert type(msgId) in (str, unicode)
                assert type(user) in (str, unicode)
                assert type(text) in (str, unicode)
            else:
                # python3.x
                self.assertIs(type(msgId), str)
                self.assertIs(type(user), str)
                self.assertIs(type(text), str)


if __name__ == '__main__':
    unittest.main()
