import unittest

import btceapi


class TestScraping(unittest.TestCase):
    def test_scrape_main_page(self):
        mainPage = btceapi.scrapeMainPage()
        for message in mainPage.messages:
            msgId, user, time, text = message
            print "%s %s: %s" % (time, user, text)


if __name__ == '__main__':
    unittest.main()
