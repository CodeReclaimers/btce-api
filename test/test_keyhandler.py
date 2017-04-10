import unittest
import tempfile
from btceapi.keyhandler import KeyData, AbstractKeyHandler, KeyHandler, InvalidNonceException


class TestKeyData(unittest.TestCase):
    def test_setNonce(self):
        data = KeyData('secret', 1)

        # happy path
        newNonce = 28
        self.assertEqual(data.setNonce(newNonce), newNonce)

        # negative nonce
        self.assertRaises(InvalidNonceException, data.setNonce, 0)

        # non-increasing nonce
        self.assertRaises(InvalidNonceException, data.setNonce, newNonce)

        # over the max value
        self.assertRaises(InvalidNonceException, data.setNonce, 4294967295)

    def test_incrementNonce(self):
        # happy path
        self.assertEqual(KeyData('secret', 1).incrementNonce(), 2)

        # over the max value
        data = KeyData('secret', 4294967294)
        self.assertRaises(InvalidNonceException, data.incrementNonce)


# we need a dummy key handler class to test on
class DummyKeyHandler(AbstractKeyHandler):
    def __init__(self):
        self.keysLoaded = False
        self.datastoreUpdated = False
        super(DummyKeyHandler, self).__init__()

    def _loadKeys(self):
        self.keysLoaded = True

    def _updateDatastore(self):
        self.datastoreUpdated = True


class TestAbstractKeyHandler(unittest.TestCase):
    def test_init(self):
        # test it loads the keys from the datastore
        handler = DummyKeyHandler()
        assert handler.keysLoaded

    def test_keys(self):
        # incidentally tests addKey, too
        self.assertEqual(set(self._handler_with_keys().keys), set(('k2', 'k1')))

    def test___del__(self):
        handler = DummyKeyHandler()
        handler.__del__()
        assert handler.datastoreUpdated

    def test___exit__(self):
        handler = DummyKeyHandler()
        handler.__exit__('type', 'value', 'traceback')
        assert handler.datastoreUpdated

    def test_close(self):
        handler = DummyKeyHandler()
        handler.close()
        assert handler.datastoreUpdated

    def test___enter__(self):
        handler = DummyKeyHandler()
        self.assertEqual(handler.__enter__(), handler)

    def test_getKey(self):
        handler = self._handler_with_keys()

        # happy path
        self.assertEqual(handler.getKey('k1').nonce, 3)

        # unknown key
        self.assertRaises(KeyError, handler.getNextNonce, 'i_dont_exist')

    def test_getNextNonce(self):
        self.assertEqual(self._handler_with_keys().getNextNonce('k2'), 29)

    def test_setNextNonce(self):
        self.assertEqual(self._handler_with_keys().setNextNonce('k1', 82), 82)

    def _handler_with_keys(self):
        handler = DummyKeyHandler()
        return handler.addKey('k1', 'secret1', 3).addKey('k2', 'secret2', 28)


class TestKeyHandler(unittest.TestCase):
    def test_save(self):
        _, filename = tempfile.mkstemp()

        handler = KeyHandler(filename=filename)
        handler.addKey('k1', 'secret1', 3).addKey('k2', 'secret2', 28)

        handler.close()

        allowed_content = ('k2\nsecret2\n28\nk1\nsecret1\n3\n',
                           'k1\nsecret1\n3\nk2\nsecret2\n28\n')
        with open(filename) as saved_file:
            self.assertTrue(saved_file.read() in allowed_content)

    def test_parse(self):
        _, filename = tempfile.mkstemp()

        with open(filename, 'w') as input_file:
            input_file.write('k2\nsecret2\n28\nk1\nsecret1\n3\n')

        handler = KeyHandler(filename=filename)

        self.assertEqual(set(handler.keys), set(['k2', 'k1']))


if __name__ == '__main__':
    unittest.main()
