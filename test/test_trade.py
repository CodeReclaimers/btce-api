import os
import unittest

import btceapi

TEST_KEY_FILE = os.path.join(os.path.dirname(__file__), "test-keys.txt")


class TestTrade(unittest.TestCase):
    def setUp(self):
        if not os.path.isfile(TEST_KEY_FILE):
            self.skipTest("No test keys found")

        self.key_handler = btceapi.KeyHandler(TEST_KEY_FILE)
        self.connection = btceapi.BTCEConnection()

    def tearDown(self):
        self.connection.close()
        self.connection = None
        self.key_handler.close()

    def test_construction(self):
        keys = list(self.key_handler.keys)
        t = btceapi.TradeAPI(keys[0], self.key_handler, self.connection)

    def test_key_info(self):
        for key in self.key_handler.keys:
            t = btceapi.TradeAPI(key, self.key_handler, self.connection)
            r = t.getInfo()


if __name__ == '__main__':
    unittest.main()
